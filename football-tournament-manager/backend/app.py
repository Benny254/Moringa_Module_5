from flask import Flask, jsonify
from flask_restful import Api

from config import Config
from extensions import db, migrate, jwt, cors

from resources.auth import RegisterResource, LoginResource, MeResource
from resources.users import UserListResource, UserResource
from resources.coaches import CoachListResource, CoachResource
from resources.teams import TeamListResource, TeamResource
from resources.tournaments import TournamentListResource, TournamentResource
from resources.registrations import RegistrationListResource, RegistrationResource
from resources.matches import MatchListResource, MatchResource
from resources.reports import (
    TeamsInTournamentResource,
    BiggestTournamentResource,
    BusyCoachesResource,
    TopTeamsResource,
    RecentRegistrationsResource,
)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, origins=app.config["CORS_ORIGINS"], supports_credentials=True)

    api = Api(app)

    # Auth
    api.add_resource(RegisterResource, "/api/auth/register")
    api.add_resource(LoginResource, "/api/auth/login")
    api.add_resource(MeResource, "/api/auth/me")

    # Users
    api.add_resource(UserListResource, "/api/users")
    api.add_resource(UserResource, "/api/users/<int:user_id>")

    # Coaches
    api.add_resource(CoachListResource, "/api/coaches")
    api.add_resource(CoachResource, "/api/coaches/<int:coach_id>")

    # Teams
    api.add_resource(TeamListResource, "/api/teams")
    api.add_resource(TeamResource, "/api/teams/<int:team_id>")

    # Tournaments
    api.add_resource(TournamentListResource, "/api/tournaments")
    api.add_resource(TournamentResource, "/api/tournaments/<int:tournament_id>")

    # Registrations
    api.add_resource(RegistrationListResource, "/api/registrations")
    api.add_resource(RegistrationResource, "/api/registrations/<int:registration_id>")

    # Matches
    api.add_resource(MatchListResource, "/api/matches")
    api.add_resource(MatchResource, "/api/matches/<int:match_id>")

    # Reports (5 advanced queries)
    api.add_resource(TeamsInTournamentResource, "/api/reports/tournaments/<int:tournament_id>/teams")
    api.add_resource(BiggestTournamentResource, "/api/reports/biggest-tournament")
    api.add_resource(BusyCoachesResource, "/api/reports/busy-coaches")
    api.add_resource(TopTeamsResource, "/api/reports/top-teams")
    api.add_resource(RecentRegistrationsResource, "/api/reports/recent-registrations")

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok"})

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"message": "Resource not found"}), 404

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"message": "Bad request"}), 400

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"message": "Internal server error"}), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
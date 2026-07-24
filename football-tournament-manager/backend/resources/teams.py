from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from extensions import db
from models import Team
from schemas import team_schema, teams_schema
from utils import paginate_query, roles_required
from config import Config


class TeamListResource(Resource):
    def get(self):
        query = db.select(Team).order_by(Team.id)
        return paginate_query(
            query, teams_schema,
            Config.DEFAULT_PAGE, Config.DEFAULT_PER_PAGE, Config.MAX_PER_PAGE,
        ), 200

    @roles_required("admin", "manager")
    def post(self):
        payload = request.get_json() or {}
        try:
            data = team_schema.load(payload, partial=("coach",))
        except ValidationError as err:
            return {"errors": err.messages}, 400

        team = Team(**{k: v for k, v in data.items() if k != "coach"})
        db.session.add(team)
        db.session.commit()
        return team_schema.dump(team), 201


class TeamResource(Resource):
    def get(self, team_id):
        team = Team.query.get_or_404(team_id)
        return team_schema.dump(team), 200

    @roles_required("admin", "manager")
    def put(self, team_id):
        team = Team.query.get_or_404(team_id)
        payload = request.get_json() or {}
        for field in ("name", "short_code", "city", "founded_year", "logo_url", "coach_id"):
            if field in payload:
                setattr(team, field, payload[field])
        db.session.commit()
        return team_schema.dump(team), 200

    @roles_required("admin")
    def delete(self, team_id):
        team = Team.query.get_or_404(team_id)
        db.session.delete(team)
        db.session.commit()
        return {"message": "Team deleted"}, 200
from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from extensions import db
from models import Tournament
from schemas import tournament_schema, tournaments_schema
from utils import paginate_query, roles_required
from config import Config


class TournamentListResource(Resource):
    def get(self):
        query = db.select(Tournament).order_by(Tournament.id)
        return paginate_query(
            query, tournaments_schema,
            Config.DEFAULT_PAGE, Config.DEFAULT_PER_PAGE, Config.MAX_PER_PAGE,
        ), 200

    @roles_required("admin", "manager")
    def post(self):
        payload = request.get_json() or {}
        try:
            data = tournament_schema.load(payload)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        tournament = Tournament(**data)
        db.session.add(tournament)
        db.session.commit()
        return tournament_schema.dump(tournament), 201


class TournamentResource(Resource):
    def get(self, tournament_id):
        tournament = Tournament.query.get_or_404(tournament_id)
        return tournament_schema.dump(tournament), 200

    @roles_required("admin", "manager")
    def put(self, tournament_id):
        tournament = Tournament.query.get_or_404(tournament_id)
        payload = request.get_json() or {}
        for field in ("name", "season", "location", "start_date", "end_date", "status"):
            if field in payload:
                setattr(tournament, field, payload[field])
        db.session.commit()
        return tournament_schema.dump(tournament), 200

    @roles_required("admin")
    def delete(self, tournament_id):
        tournament = Tournament.query.get_or_404(tournament_id)
        db.session.delete(tournament)
        db.session.commit()
        return {"message": "Tournament deleted"}, 200
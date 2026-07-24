from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from extensions import db
from models import Coach
from schemas import coach_schema, coaches_schema
from utils import paginate_query, roles_required
from config import Config


class CoachListResource(Resource):
    def get(self):
        query = db.select(Coach).order_by(Coach.id)
        return paginate_query(
            query, coaches_schema,
            Config.DEFAULT_PAGE, Config.DEFAULT_PER_PAGE, Config.MAX_PER_PAGE,
        ), 200

    @roles_required("admin", "manager")
    def post(self):
        payload = request.get_json() or {}
        try:
            data = coach_schema.load(payload, partial=("teams",))
        except ValidationError as err:
            return {"errors": err.messages}, 400

        coach = Coach(**{k: v for k, v in data.items() if k != "teams"})
        db.session.add(coach)
        db.session.commit()
        return coach_schema.dump(coach), 201


class CoachResource(Resource):
    def get(self, coach_id):
        coach = Coach.query.get_or_404(coach_id)
        return coach_schema.dump(coach), 200

    @roles_required("admin", "manager")
    def put(self, coach_id):
        coach = Coach.query.get_or_404(coach_id)
        payload = request.get_json() or {}
        for field in ("name", "license_level", "years_experience"):
            if field in payload:
                setattr(coach, field, payload[field])
        db.session.commit()
        return coach_schema.dump(coach), 200

    @roles_required("admin")
    def delete(self, coach_id):
        coach = Coach.query.get_or_404(coach_id)
        db.session.delete(coach)
        db.session.commit()
        return {"message": "Coach deleted"}, 200
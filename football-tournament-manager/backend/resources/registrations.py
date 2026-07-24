from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from extensions import db
from models import Registration
from schemas import registration_schema, registrations_schema
from utils import paginate_query, roles_required
from config import Config


class RegistrationListResource(Resource):
    def get(self):
        query = db.select(Registration).order_by(Registration.id)

        tournament_id = request.args.get("tournament_id")
        team_id = request.args.get("team_id")
        if tournament_id:
            query = query.where(Registration.tournament_id == int(tournament_id))
        if team_id:
            query = query.where(Registration.team_id == int(team_id))

        return paginate_query(
            query, registrations_schema,
            Config.DEFAULT_PAGE, Config.DEFAULT_PER_PAGE, Config.MAX_PER_PAGE,
        ), 200

    @roles_required("admin", "manager")
    def post(self):
        payload = request.get_json() or {}
        try:
            data = registration_schema.load(payload, partial=("team", "tournament"))
        except ValidationError as err:
            return {"errors": err.messages}, 400

        existing = Registration.query.filter_by(
            team_id=data["team_id"], tournament_id=data["tournament_id"]
        ).first()
        if existing:
            return {"message": "Team is already registered for this tournament"}, 409

        registration = Registration(**{k: v for k, v in data.items() if k not in ("team", "tournament")})
        db.session.add(registration)
        db.session.commit()
        return registration_schema.dump(registration), 201


class RegistrationResource(Resource):
    def get(self, registration_id):
        registration = Registration.query.get_or_404(registration_id)
        return registration_schema.dump(registration), 200

    @roles_required("admin", "manager")
    def put(self, registration_id):
        registration = Registration.query.get_or_404(registration_id)
        payload = request.get_json() or {}
        for field in ("status", "points"):
            if field in payload:
                setattr(registration, field, payload[field])
        db.session.commit()
        return registration_schema.dump(registration), 200

    @roles_required("admin")
    def delete(self, registration_id):
        registration = Registration.query.get_or_404(registration_id)
        db.session.delete(registration)
        db.session.commit()
        return {"message": "Registration deleted"}, 200
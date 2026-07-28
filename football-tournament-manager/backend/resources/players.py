from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from extensions import db
from models import Player
from schemas import player_schema, players_schema
from utils import paginate_query, roles_required
from config import Config


class PlayerListResource(Resource):
    def get(self):
        query = db.select(Player).order_by(Player.id)
        team_id = request.args.get("team_id")
        if team_id:
            query = query.where(Player.team_id == int(team_id))
        return paginate_query(
            query, players_schema,
            Config.DEFAULT_PAGE, Config.DEFAULT_PER_PAGE, Config.MAX_PER_PAGE,
        ), 200

    @roles_required("admin", "manager")
    def post(self):
        payload = request.get_json() or {}
        try:
            data = player_schema.load(payload, partial=("team",))
        except ValidationError as err:
            return {"errors": err.messages}, 400

        player = Player(**{k: v for k, v in data.items() if k != "team"})
        db.session.add(player)
        db.session.commit()
        return player_schema.dump(player), 201


class PlayerResource(Resource):
    def get(self, player_id):
        player = Player.query.get_or_404(player_id)
        return player_schema.dump(player), 200

    @roles_required("admin", "manager")
    def put(self, player_id):
        player = Player.query.get_or_404(player_id)
        payload = request.get_json() or {}
        for field in ("name", "position", "jersey_number", "date_of_birth", "team_id"):
            if field in payload:
                setattr(player, field, payload[field])
        db.session.commit()
        return player_schema.dump(player), 200

    @roles_required("admin")
    def delete(self, player_id):
        player = Player.query.get_or_404(player_id)
        db.session.delete(player)
        db.session.commit()
        return {"message": "Player deleted"}, 200
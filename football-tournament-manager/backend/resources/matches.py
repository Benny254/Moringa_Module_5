from datetime import datetime
from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from extensions import db
from models import Match
from schemas import match_schema, matches_schema
from utils import paginate_query, roles_required
from config import Config


def parse_iso_datetime(value):
    if isinstance(value, datetime):
        return value
    # Support both "...Z" suffix and offset-aware ISO strings
    return datetime.fromisoformat(str(value).replace("Z", "+00:00"))


class MatchListResource(Resource):
    def get(self):
        query = db.select(Match).order_by(Match.match_date)

        tournament_id = request.args.get("tournament_id")
        team_id = request.args.get("team_id")
        status = request.args.get("status")
        if tournament_id:
            query = query.where(Match.tournament_id == int(tournament_id))
        if team_id:
            query = query.where(
                (Match.home_team_id == int(team_id)) | (Match.away_team_id == int(team_id))
            )
        if status:
            query = query.where(Match.status == status)

        return paginate_query(
            query, matches_schema,
            Config.DEFAULT_PAGE, Config.DEFAULT_PER_PAGE, Config.MAX_PER_PAGE,
        ), 200

    @roles_required("admin", "manager")
    def post(self):
        payload = request.get_json() or {}
        try:
            data = match_schema.load(payload, partial=("tournament", "home_team", "away_team"))
        except ValidationError as err:
            return {"errors": err.messages}, 400

        match = Match(
            tournament_id=data["tournament_id"],
            home_team_id=data["home_team_id"],
            away_team_id=data["away_team_id"],
            match_date=parse_iso_datetime(payload["match_date"]),
            venue=data.get("venue"),
            status=data.get("status", "scheduled"),
        )
        db.session.add(match)
        db.session.commit()
        return match_schema.dump(match), 201


class MatchResource(Resource):
    def get(self, match_id):
        match = Match.query.get_or_404(match_id)
        return match_schema.dump(match), 200

    @roles_required("admin", "manager")
    def put(self, match_id):
        match = Match.query.get_or_404(match_id)
        payload = request.get_json() or {}

        if "match_date" in payload:
            match.match_date = parse_iso_datetime(payload["match_date"])
        for field in ("venue", "home_score", "away_score", "status"):
            if field in payload:
                setattr(match, field, payload[field])

        db.session.commit()
        return match_schema.dump(match), 200

    @roles_required("admin")
    def delete(self, match_id):
        match = Match.query.get_or_404(match_id)
        db.session.delete(match)
        db.session.commit()
        return {"message": "Match deleted"}, 200
from flask import request
from flask_restful import Resource
from sqlalchemy import func, desc

from extensions import db
from models import Team, Tournament, Coach, Registration, Match
from utils import roles_required


class TeamsInTournamentResource(Resource):
    """1) JOIN: list all teams registered in a given tournament."""

    def get(self, tournament_id):
        rows = (
            db.session.query(Team.id, Team.name, Team.city, Registration.status, Registration.points)
            .join(Registration, Registration.team_id == Team.id)
            .filter(Registration.tournament_id == tournament_id)
            .order_by(desc(Registration.points))
            .all()
        )
        return {
            "tournament_id": tournament_id,
            "teams": [
                {
                    "id": r.id,
                    "name": r.name,
                    "city": r.city,
                    "status": r.status,
                    "points": r.points,
                }
                for r in rows
            ],
        }, 200


class BiggestTournamentResource(Resource):
    """2) COUNT + GROUP BY: tournament(s) with the most registered teams."""

    def get(self):
        rows = (
            db.session.query(
                Tournament.id,
                Tournament.name,
                func.count(Registration.id).label("team_count"),
            )
            .join(Registration, Registration.tournament_id == Tournament.id)
            .group_by(Tournament.id)
            .order_by(desc("team_count"))
            .limit(5)
            .all()
        )
        return {
            "tournaments": [
                {"id": r.id, "name": r.name, "team_count": r.team_count} for r in rows
            ]
        }, 200


class BusyCoachesResource(Resource):
    """3) HAVING: coaches managing more than N teams (default 1)."""

    def get(self):
        min_teams = int(request.args.get("min_teams", 1))
        rows = (
            db.session.query(
                Coach.id, Coach.name, func.count(Team.id).label("team_count")
            )
            .join(Team, Team.coach_id == Coach.id)
            .group_by(Coach.id)
            .having(func.count(Team.id) > min_teams)
            .order_by(desc("team_count"))
            .all()
        )
        return {
            "min_teams": min_teams,
            "coaches": [
                {"id": r.id, "name": r.name, "team_count": r.team_count} for r in rows
            ],
        }, 200


class TopTeamsResource(Resource):
    """4) ORDER BY aggregate: top teams by total registration points across all tournaments."""

    def get(self):
        limit = int(request.args.get("limit", 10))
        rows = (
            db.session.query(
                Team.id, Team.name, func.coalesce(func.sum(Registration.points), 0).label("total_points")
            )
            .outerjoin(Registration, Registration.team_id == Team.id)
            .group_by(Team.id)
            .order_by(desc("total_points"))
            .limit(limit)
            .all()
        )
        return {
            "teams": [
                {"id": r.id, "name": r.name, "total_points": int(r.total_points)} for r in rows
            ]
        }, 200


class RecentRegistrationsResource(Resource):
    """5) Relationship filtering: most recent registrations across the system."""

    def get(self):
        limit = int(request.args.get("limit", 10))
        registrations = (
            Registration.query.order_by(desc(Registration.registration_date))
            .limit(limit)
            .all()
        )
        return {
            "registrations": [
                {
                    "id": r.id,
                    "team": r.team.name if r.team else None,
                    "tournament": r.tournament.name if r.tournament else None,
                    "status": r.status,
                    "registration_date": r.registration_date.isoformat() if r.registration_date else None,
                }
                for r in registrations
            ]
        }, 200
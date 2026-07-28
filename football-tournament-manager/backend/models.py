from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db


def now_utc():
    return datetime.now(timezone.utc)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="player")  # admin | manager | player
    created_at = db.Column(db.DateTime, default=now_utc)

    # One-to-one: User <-> Profile
    profile = db.relationship(
        "Profile", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    # One-to-many: User -> Coach profiles they might hold (a user can be linked to one coach record)
    coach = db.relationship(
        "Coach", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"


class Profile(db.Model):
    __tablename__ = "profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    full_name = db.Column(db.String(120))
    bio = db.Column(db.Text)
    avatar_url = db.Column(db.String(255))
    phone = db.Column(db.String(30))
    country = db.Column(db.String(80))

    user = db.relationship("User", back_populates="profile")


class Coach(db.Model):
    __tablename__ = "coaches"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=True)
    name = db.Column(db.String(120), nullable=False)
    license_level = db.Column(db.String(50))  # e.g. UEFA A, UEFA B, CAF C
    years_experience = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=now_utc)

    user = db.relationship("User", back_populates="coach")
    # One-to-many: Coach -> Teams
    teams = db.relationship("Team", back_populates="coach")

    def __repr__(self):
        return f"<Coach {self.name}>"


class Team(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    short_code = db.Column(db.String(10))
    city = db.Column(db.String(80))
    founded_year = db.Column(db.Integer)
    logo_url = db.Column(db.String(255))
    coach_id = db.Column(db.Integer, db.ForeignKey("coaches.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=now_utc)

    coach = db.relationship("Coach", back_populates="teams")
    # Many-to-many via association object Registration
    registrations = db.relationship(
        "Registration", back_populates="team", cascade="all, delete-orphan"
    )
    tournaments = db.relationship(
        "Tournament", secondary="registrations", viewonly=True, back_populates="teams"
    )

    home_matches = db.relationship(
        "Match", foreign_keys="Match.home_team_id", back_populates="home_team"
    )
    away_matches = db.relationship(
        "Match", foreign_keys="Match.away_team_id", back_populates="away_team"
    )
    players = db.relationship(
        "Player", back_populates="team", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Team {self.name}>"


class Tournament(db.Model):
    __tablename__ = "tournaments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    season = db.Column(db.String(20))
    location = db.Column(db.String(120))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20), default="upcoming")  # upcoming | ongoing | completed
    created_at = db.Column(db.DateTime, default=now_utc)

    registrations = db.relationship(
        "Registration", back_populates="tournament", cascade="all, delete-orphan"
    )
    teams = db.relationship(
        "Team", secondary="registrations", viewonly=True, back_populates="tournaments"
    )
    matches = db.relationship(
        "Match", back_populates="tournament", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Tournament {self.name}>"


class Registration(db.Model):
    """Association object for the Team <-> Tournament many-to-many relationship."""

    __tablename__ = "registrations"

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=False)
    tournament_id = db.Column(db.Integer, db.ForeignKey("tournaments.id"), nullable=False)
    registration_date = db.Column(db.DateTime, default=now_utc)
    status = db.Column(db.String(20), default="pending")  # pending | approved | rejected
    points = db.Column(db.Integer, default=0)

    team = db.relationship("Team", back_populates="registrations")
    tournament = db.relationship("Tournament", back_populates="registrations")

    __table_args__ = (
        db.UniqueConstraint("team_id", "tournament_id", name="uq_team_tournament"),
    )


class Match(db.Model):
    __tablename__ = "matches"

    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey("tournaments.id"), nullable=False)
    home_team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=False)
    away_team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=False)
    match_date = db.Column(db.DateTime, nullable=False)
    venue = db.Column(db.String(150))
    home_score = db.Column(db.Integer)
    away_score = db.Column(db.Integer)
    status = db.Column(db.String(20), default="scheduled")  # scheduled | live | completed

    tournament = db.relationship("Tournament", back_populates="matches")
    home_team = db.relationship("Team", foreign_keys=[home_team_id], back_populates="home_matches")
    away_team = db.relationship("Team", foreign_keys=[away_team_id], back_populates="away_matches")

class Player(db.Model):
    __tablename__ = "players"

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    position = db.Column(db.String(30))  # Goalkeeper | Defender | Midfielder | Forward
    jersey_number = db.Column(db.Integer)
    date_of_birth = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=now_utc)

    team = db.relationship("Team", back_populates="players")

    __table_args__ = (
        db.UniqueConstraint("team_id", "jersey_number", name="uq_team_jersey"),
    )

    def __repr__(self):
        return f"<Player {self.name} (#{self.jersey_number})>"
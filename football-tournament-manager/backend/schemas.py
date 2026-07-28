from marshmallow import Schema, fields, validate


class ProfileSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    full_name = fields.Str()
    bio = fields.Str(allow_none=True)
    avatar_url = fields.Str(allow_none=True)
    phone = fields.Str(allow_none=True)
    country = fields.Str(allow_none=True)


class UserBriefSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str()
    role = fields.Str()


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    password = fields.Str(load_only=True, validate=validate.Length(min=6))
    role = fields.Str(validate=validate.OneOf(["admin", "manager", "player"]))
    created_at = fields.DateTime(dump_only=True)
    profile = fields.Nested(ProfileSchema, dump_only=True)
    full_name = fields.Str(load_only=True, required=False)


class CoachBriefSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    license_level = fields.Str(allow_none=True)


class CoachSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(allow_none=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=120))
    license_level = fields.Str(allow_none=True)
    years_experience = fields.Int()
    created_at = fields.DateTime(dump_only=True)
    teams = fields.List(fields.Nested("TeamBriefSchema"), dump_only=True)


class TeamBriefSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    short_code = fields.Str(allow_none=True)
    city = fields.Str(allow_none=True)
    logo_url = fields.Str(allow_none=True)


class TeamSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=120))
    short_code = fields.Str(allow_none=True)
    city = fields.Str(allow_none=True)
    founded_year = fields.Int(allow_none=True)
    logo_url = fields.Str(allow_none=True)
    coach_id = fields.Int(allow_none=True)
    coach = fields.Nested(CoachBriefSchema, dump_only=True)
    created_at = fields.DateTime(dump_only=True)


class TournamentBriefSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    season = fields.Str(allow_none=True)
    status = fields.Str()


class TournamentSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=150))
    season = fields.Str(allow_none=True)
    location = fields.Str(allow_none=True)
    start_date = fields.Date(allow_none=True)
    end_date = fields.Date(allow_none=True)
    status = fields.Str(validate=validate.OneOf(["upcoming", "ongoing", "completed"]))
    created_at = fields.DateTime(dump_only=True)


class RegistrationSchema(Schema):
    id = fields.Int(dump_only=True)
    team_id = fields.Int(required=True)
    tournament_id = fields.Int(required=True)
    registration_date = fields.DateTime(dump_only=True)
    status = fields.Str(validate=validate.OneOf(["pending", "approved", "rejected"]))
    points = fields.Int()
    team = fields.Nested(TeamBriefSchema, dump_only=True)
    tournament = fields.Nested(TournamentBriefSchema, dump_only=True)


class MatchSchema(Schema):
    id = fields.Int(dump_only=True)
    tournament_id = fields.Int(required=True)
    home_team_id = fields.Int(required=True)
    away_team_id = fields.Int(required=True)
    match_date = fields.DateTime(required=True)
    venue = fields.Str(allow_none=True)
    home_score = fields.Int(allow_none=True)
    away_score = fields.Int(allow_none=True)
    status = fields.Str(validate=validate.OneOf(["scheduled", "live", "completed"]))
    tournament = fields.Nested(TournamentBriefSchema, dump_only=True)
    home_team = fields.Nested(TeamBriefSchema, dump_only=True)
    away_team = fields.Nested(TeamBriefSchema, dump_only=True)


class PlayerSchema(Schema):
    id = fields.Int(dump_only=True)
    team_id = fields.Int(required=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=120))
    position = fields.Str(
        allow_none=True,
        validate=validate.OneOf(["Goalkeeper", "Defender", "Midfielder", "Forward"]),
    )
    jersey_number = fields.Int(allow_none=True)
    date_of_birth = fields.Date(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    team = fields.Nested(TeamBriefSchema, dump_only=True)


player_schema = PlayerSchema()
players_schema = PlayerSchema(many=True)    
user_schema = UserSchema()
users_schema = UserSchema(many=True)
profile_schema = ProfileSchema()
coach_schema = CoachSchema()
coaches_schema = CoachSchema(many=True)
team_schema = TeamSchema()
teams_schema = TeamSchema(many=True)
tournament_schema = TournamentSchema()
tournaments_schema = TournamentSchema(many=True)
registration_schema = RegistrationSchema()
registrations_schema = RegistrationSchema(many=True)
match_schema = MatchSchema()
matches_schema = MatchSchema(many=True)
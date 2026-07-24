"""
Seed the database with realistic sample data.
Usage: python seed.py  (run after flask db upgrade)
"""
import random
from datetime import timedelta
from faker import Faker

from app import create_app
from extensions import db
from models import User, Profile, Coach, Team, Tournament, Registration, Match

fake = Faker()


def seed():
    print("Clearing existing data...")
    Match.query.delete()
    Registration.query.delete()
    Team.query.delete()
    Coach.query.delete()
    Tournament.query.delete()
    Profile.query.delete()
    User.query.delete()
    db.session.commit()

    print("Creating users...")
    admin = User(username="admin", email="admin@tournament.com", role="admin")
    admin.set_password("admin123")
    db.session.add(admin)
    db.session.flush()
    db.session.add(Profile(user_id=admin.id, full_name="System Administrator", country="Kenya"))

    manager = User(username="manager", email="manager@tournament.com", role="manager")
    manager.set_password("manager123")
    db.session.add(manager)
    db.session.flush()
    db.session.add(Profile(user_id=manager.id, full_name="Tournament Manager", country="Kenya"))

    users = [admin, manager]
    for _ in range(45):
        username = fake.unique.user_name()
        user = User(username=username, email=fake.unique.email(), role="player")
        user.set_password("password123")
        db.session.add(user)
        db.session.flush()
        db.session.add(
            Profile(
                user_id=user.id,
                full_name=fake.name(),
                bio=fake.sentence(nb_words=12),
                country=fake.country(),
                phone=fake.phone_number()[:30],
            )
        )
        users.append(user)
    db.session.commit()

    print("Creating coaches...")
    coaches = []
    licenses = ["UEFA Pro", "UEFA A", "UEFA B", "CAF A", "CAF B"]
    for _ in range(8):
        coach = Coach(
            name=fake.name(),
            license_level=random.choice(licenses),
            years_experience=random.randint(1, 25),
        )
        db.session.add(coach)
        coaches.append(coach)
    db.session.commit()

    print("Creating teams...")
    team_names = [
        "Nairobi Chapel", "Reject Fc", "Boom Family", "Waves Fc",
        "Karen Hospital Fc", "Casablanca", "Upper Karen", "RGC Sports",
        "111 Pro", "111 State", "G-star", "Young shines", "Kariobangi Sharks", "Mathare United", "Tusker Fc",
    ]
    teams = []
    for name in team_names:
        team = Team(
            name=name,
            short_code=name.split()[-1][:3].upper(),
            city=fake.city(),
            founded_year=random.randint(1970, 2015),
            coach_id=random.choice(coaches).id,
        )
        db.session.add(team)
        teams.append(team)
    db.session.commit()

    print("Creating tournaments...")
    tournament_data = [
        ("Contem Cup", "2025/26"),
        ("Fivestarz Champions League", "2025/26"),
        ("Youth Invitational", "2026"),
        ("City Derby Series", "2025"),
    ]
    tournaments = []
    for name, season in tournament_data:
        start = fake.date_between(start_date="-60d", end_date="+30d")
        tournament = Tournament(
            name=name,
            season=season,
            location=fake.city(),
            start_date=start,
            end_date=start + timedelta(days=random.randint(20, 90)),
            status=random.choice(["upcoming", "ongoing", "completed"]),
        )
        db.session.add(tournament)
        tournaments.append(tournament)
    db.session.commit()

    print("Creating registrations...")
    for tournament in tournaments:
        chosen_teams = random.sample(teams, k=random.randint(6, len(teams)))
        for team in chosen_teams:
            reg = Registration(
                team_id=team.id,
                tournament_id=tournament.id,
                status=random.choice(["approved", "approved", "pending"]),
                points=random.randint(0, 30),
            )
            db.session.add(reg)
    db.session.commit()

    print("Creating matches...")
    for tournament in tournaments:
        reg_teams = [r.team for r in tournament.registrations]
        if len(reg_teams) < 2:
            continue
        for _ in range(random.randint(5, 10)):
            home, away = random.sample(reg_teams, 2)
            is_past = random.random() < 0.6
            match_date = fake.date_time_between(start_date="-30d", end_date="+30d")
            match = Match(
                tournament_id=tournament.id,
                home_team_id=home.id,
                away_team_id=away.id,
                match_date=match_date,
                venue=fake.city() + " Stadium",
                status="completed" if is_past else random.choice(["scheduled", "live"]),
                home_score=random.randint(0, 5) if is_past else None,
                away_score=random.randint(0, 5) if is_past else None,
            )
            db.session.add(match)
    db.session.commit()

    print("Seed complete.")
    print("Login with: admin / admin123  (role: admin)")
    print("       or: manager / manager123  (role: manager)")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed()
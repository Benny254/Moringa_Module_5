"""
seed.py
-------
Wipes and repopulates the database with sample users + notes so the
frontend has data to work with right away.

Run with:  python seed.py   (from inside server/, with venv active)

Test login after seeding: username "janedoe", password "password123"
(same pattern for all seeded users — see USERNAMES below).
"""
from faker import Faker

from config import app, db
from models import User, Note

fake = Faker()

USERNAMES = ["benard", "mike", "pinton", "bobmarley"]


def seed():
    with app.app_context():
        print("Clearing existing data...")
        Note.query.delete()
        User.query.delete()
        db.session.commit()

        print("Seeding users...")
        users = []
        for username in USERNAMES:
            user = User(username=username, email=f"{username}@example.com")
            user.password_hash = "password123"
            users.append(user)
        db.session.add_all(users)
        db.session.commit()

        print("Seeding notes...")
        notes = []
        for user in users:
            for _ in range(range_for_demo()):
                notes.append(Note(
                    title=fake.sentence(nb_words=4).rstrip("."),
                    content=fake.paragraph(nb_sentences=3),
                    user_id=user.id,
                ))
        db.session.add_all(notes)
        db.session.commit()

        print(f"Seeded {len(users)} users and {len(notes)} notes. Done!")


def range_for_demo():
    # A few notes per user is plenty to exercise pagination (per_page default 10)
    return fake.random_int(min=3, max=12)


if __name__ == "__main__":
    seed()
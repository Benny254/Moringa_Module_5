#!/usr/bin/env python3

from datetime import date, timedelta

from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
    print("Clearing existing data...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    print("Seeding exercises...")
    push_up = Exercise(name="Push-Up", category="strength", equipment_needed=False)
    squat = Exercise(name="Squat", category="strength", equipment_needed=False)
    running = Exercise(name="Running", category="cardio", equipment_needed=False)
    plank = Exercise(name="Plank", category="core", equipment_needed=False)
    bench_press = Exercise(
        name="Bench Press", category="strength", equipment_needed=True
    )

    db.session.add_all([push_up, squat, running, plank, bench_press])
    db.session.commit()

    print("Seeding workouts...")
    workout_1 = Workout(
        date=date.today(),
        duration_minutes=45,
        notes="Full body strength session.",
    )
    workout_2 = Workout(
        date=date.today() - timedelta(days=2),
        duration_minutes=30,
        notes="Morning cardio and core.",
    )

    db.session.add_all([workout_1, workout_2])
    db.session.commit()

    print("Linking exercises to workouts...")
    db.session.add_all(
        [
            WorkoutExercise(
                workout_id=workout_1.id, exercise_id=push_up.id, reps=15, sets=3
            ),
            WorkoutExercise(
                workout_id=workout_1.id, exercise_id=squat.id, reps=12, sets=4
            ),
            WorkoutExercise(
                workout_id=workout_1.id,
                exercise_id=bench_press.id,
                reps=10,
                sets=3,
            ),
            WorkoutExercise(
                workout_id=workout_2.id,
                exercise_id=running.id,
                duration_seconds=1200,
            ),
            WorkoutExercise(
                workout_id=workout_2.id,
                exercise_id=plank.id,
                duration_seconds=60,
                sets=3,
            ),
        ]
    )
    db.session.commit()

    print("Done seeding!")
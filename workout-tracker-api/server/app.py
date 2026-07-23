from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models import db, Exercise, Workout, WorkoutExercise
from schemas import (
    ExerciseSchema,
    ExerciseDetailSchema,
    WorkoutSchema,
    WorkoutDetailSchema,
    WorkoutExerciseSchema,
)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)
db.init_app(app)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
exercise_detail_schema = ExerciseDetailSchema()

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_detail_schema = WorkoutDetailSchema()

workout_exercise_schema = WorkoutExerciseSchema()


def error_response(message, status=400):
    errors = message if isinstance(message, list) else [message]
    return make_response(jsonify({"errors": errors}), status)


@app.route("/workouts", methods=["GET", "POST"])
def workouts():
    if request.method == "GET":
        return jsonify(workouts_schema.dump(Workout.query.all())), 200

    data = request.get_json() or {}
    try:
        validated = workout_schema.load(data)
    except ValidationError as err:
        return error_response(err.messages, 400)

    workout = Workout(
        date=validated["date"],
        duration_minutes=validated["duration_minutes"],
        notes=validated.get("notes"),
    )

    try:
        db.session.add(workout)
        db.session.commit()
    except (IntegrityError, ValueError) as err:
        db.session.rollback()
        return error_response(str(err), 400)

    return jsonify(workout_schema.dump(workout)), 201


@app.route("/workouts/<int:id>", methods=["GET", "DELETE"])
def workout_by_id(id):
    workout = db.session.get(Workout, id)
    if workout is None:
        return error_response("Workout not found.", 404)

    if request.method == "GET":
        return jsonify(workout_detail_schema.dump(workout)), 200

    # DELETE - cascade removes associated WorkoutExercises (stretch goal)
    db.session.delete(workout)
    db.session.commit()
    return make_response("", 204)


@app.route("/exercises", methods=["GET", "POST"])
def exercises():
    if request.method == "GET":
        return jsonify(exercises_schema.dump(Exercise.query.all())), 200

    data = request.get_json() or {}
    try:
        validated = exercise_schema.load(data)
    except ValidationError as err:
        return error_response(err.messages, 400)

    exercise = Exercise(
        name=validated["name"],
        category=validated["category"],
        equipment_needed=validated.get("equipment_needed", False),
    )

    try:
        db.session.add(exercise)
        db.session.commit()
    except (IntegrityError, ValueError) as err:
        db.session.rollback()
        return error_response(str(err), 400)

    return jsonify(exercise_schema.dump(exercise)), 201


@app.route("/exercises/<int:id>", methods=["GET", "DELETE"])
def exercise_by_id(id):
    exercise = db.session.get(Exercise, id)
    if exercise is None:
        return error_response("Exercise not found.", 404)

    if request.method == "GET":
        return jsonify(exercise_detail_schema.dump(exercise)), 200

    # DELETE - cascade removes associated WorkoutExercises (stretch goal)
    db.session.delete(exercise)
    db.session.commit()
    return make_response("", 204)


@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"],
)
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)

    if workout is None:
        return error_response("Workout not found.", 404)
    if exercise is None:
        return error_response("Exercise not found.", 404)

    data = request.get_json() or {}
    try:
        validated = workout_exercise_schema.load(data)
    except ValidationError as err:
        return error_response(err.messages, 400)

    workout_exercise = WorkoutExercise(
        workout_id=workout.id,
        exercise_id=exercise.id,
        reps=validated.get("reps"),
        sets=validated.get("sets"),
        duration_seconds=validated.get("duration_seconds"),
    )

    try:
        db.session.add(workout_exercise)
        db.session.commit()
    except (IntegrityError, ValueError) as err:
        db.session.rollback()
        return error_response(str(err), 400)

    return jsonify(workout_exercise_schema.dump(workout_exercise)), 201


if __name__ == "__main__":
    app.run(port=5555, debug=True)
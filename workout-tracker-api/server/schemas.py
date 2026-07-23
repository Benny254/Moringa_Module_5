from marshmallow import Schema, fields, validate

CATEGORY_CHOICES = ["cardio", "strength", "flexibility", "balance", "core"]


class ExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    category = fields.String(
        required=True, validate=validate.OneOf(CATEGORY_CHOICES)
    )
    equipment_needed = fields.Boolean(load_default=False)


class WorkoutSchema(Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Integer(
        required=True, validate=validate.Range(min=1, max=600)
    )
    notes = fields.String(allow_none=True, validate=validate.Length(max=1000))


class WorkoutExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    workout_id = fields.Integer(dump_only=True)
    exercise_id = fields.Integer(dump_only=True)
    reps = fields.Integer(validate=validate.Range(min=0), allow_none=True)
    sets = fields.Integer(validate=validate.Range(min=0), allow_none=True)
    duration_seconds = fields.Integer(
        validate=validate.Range(min=0), allow_none=True
    )
    exercise = fields.Nested(ExerciseSchema, dump_only=True)
    workout = fields.Nested(WorkoutSchema, dump_only=True)


class WorkoutDetailSchema(WorkoutSchema):
    workout_exercises = fields.List(
        fields.Nested(WorkoutExerciseSchema(exclude=("workout",))),
        dump_only=True,
    )


class ExerciseDetailSchema(ExerciseSchema):
    workout_exercises = fields.List(
        fields.Nested(WorkoutExerciseSchema(exclude=("exercise",))),
        dump_only=True,
    )
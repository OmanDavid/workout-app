from marshmallow import Schema, fields, validate


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, error='Name cannot be empty.')
    )
    category = fields.Str(
        required=True,
        validate=validate.Length(min=1, error='Category cannot be empty.')
    )
    equipment_needed = fields.Bool(load_default=False)


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(
        allow_none=True,
        validate=validate.Range(min=0, error='Reps must be zero or greater.')
    )
    sets = fields.Int(
        allow_none=True,
        validate=validate.Range(min=0, error='Sets must be zero or greater.')
    )
    duration_seconds = fields.Int(
        allow_none=True,
        validate=validate.Range(min=0, error='Duration (seconds) must be zero or greater.')
    )
    exercise = fields.Nested(ExerciseSchema, dump_only=True)


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(
        required=True,
        validate=validate.Range(min=1, error='Duration must be a positive number of minutes.')
    )
    notes = fields.Str(allow_none=True)
    workout_exercises = fields.List(fields.Nested(WorkoutExerciseSchema), dump_only=True)


exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()
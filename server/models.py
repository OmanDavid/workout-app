from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint

# SQLAlchemy database instance for Flask app models
db = SQLAlchemy()


class Exercise(db.Model):
    # Table for exercise definitions, one row per exercise
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False)

    # Relationship: this exercise can appear in many workout entries
    workout_exercises = db.relationship(
        'WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan'
    )
    # Many-to-many view: workouts that include this exercise via workout_exercises
    workouts = db.relationship(
        'Workout', secondary='workout_exercises', back_populates='exercises', viewonly=True
    )

    # model validations
    @validates('name')
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError('Exercise name cannot be empty.')
        return value.strip()

    @validates('category')
    def validate_category(self, key, value):
        if not value or not value.strip():
            raise ValueError('Exercise category cannot be empty.')
        return value.strip()

    def __repr__(self):
        return f'<Exercise {self.id}: {self.name}>'


class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    # Ensure each workout has a positive duration
    __table_args__ = (
        CheckConstraint('duration_minutes > 0', name='check_duration_positive'),
    )

    # Relationship: this workout contains many workout-exercise entries
    workout_exercises = db.relationship(
        'WorkoutExercise', back_populates='workout', cascade='all, delete-orphan'
    )
    # has many Exercises through WorkoutExercises
    exercises = db.relationship(
        'Exercise', secondary='workout_exercises', back_populates='workouts', viewonly=True
    )

    # model validation
    @validates('duration_minutes')
    def validate_duration(self, key, value):
        if value is None or value <= 0:
            raise ValueError('Duration must be a positive number of minutes.')
        return value

    def __repr__(self):
        return f'<Workout {self.id} on {self.date}>'


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    # Allow null values but prevent negative reps or sets
    __table_args__ = (
        CheckConstraint('reps IS NULL OR reps >= 0', name='check_reps_non_negative'),
        CheckConstraint('sets IS NULL OR sets >= 0', name='check_sets_non_negative'),
    )

    # Relationship: this entry belongs to one workout
    workout = db.relationship('Workout', back_populates='workout_exercises')
    # belongs to Exercise
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    # model validation
    @validates('reps')
    def validate_reps(self, key, value):
        if value is not None and value < 0:
            raise ValueError('Reps cannot be negative.')
        return value

    @validates('sets')
    def validate_sets(self, key, value):
        if value is not None and value < 0:
            raise ValueError('Sets cannot be negative.')
        return value

    def __repr__(self):
        return f'<WorkoutExercise {self.id}: workout={self.workout_id} exercise={self.exercise_id}>'
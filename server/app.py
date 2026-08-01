from flask import Flask, request, jsonify
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models import db, Exercise, Workout, WorkoutExercise
from schemas import (
    exercise_schema, exercises_schema,
    workout_schema, workouts_schema,
    workout_exercise_schema
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)


# ------------------------- Workouts -------------------------

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return jsonify({'error': 'Workout not found'}), 404
    return jsonify(workout_schema.dump(workout)), 200


@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json() or {}
    try:
        validated = workout_schema.load(data)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    try:
        workout = Workout(
            date=validated['date'],
            duration_minutes=validated['duration_minutes'],
            notes=validated.get('notes')
        )
        db.session.add(workout)
        db.session.commit()
    except (ValueError, IntegrityError) as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

    return jsonify(workout_schema.dump(workout)), 201


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return jsonify({'error': 'Workout not found'}), 404
    db.session.delete(workout)
    db.session.commit()
    return '', 204


# ------------------------- Exercises -------------------------

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({'error': 'Exercise not found'}), 404

    data = exercise_schema.dump(exercise)
    data['workouts'] = [
        {'id': w.id, 'date': w.date.isoformat(), 'duration_minutes': w.duration_minutes}
        for w in exercise.workouts
    ]
    return jsonify(data), 200


@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json() or {}
    try:
        validated = exercise_schema.load(data)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    try:
        exercise = Exercise(
            name=validated['name'],
            category=validated['category'],
            equipment_needed=validated.get('equipment_needed', False)
        )
        db.session.add(exercise)
        db.session.commit()
    except (ValueError, IntegrityError) as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

    return jsonify(exercise_schema.dump(exercise)), 201


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({'error': 'Exercise not found'}), 404
    db.session.delete(exercise)
    db.session.commit()
    return '', 204


# ------------------------- WorkoutExercises -------------------------

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    exercise = Exercise.query.get(exercise_id)
    if not workout or not exercise:
        return jsonify({'error': 'Workout or Exercise not found'}), 404

    data = request.get_json() or {}
    try:
        validated = workout_exercise_schema.load(data, partial=True)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    try:
        workout_exercise = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            reps=validated.get('reps'),
            sets=validated.get('sets'),
            duration_seconds=validated.get('duration_seconds')
        )
        db.session.add(workout_exercise)
        db.session.commit()
    except (ValueError, IntegrityError) as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

    return jsonify(workout_exercise_schema.dump(workout_exercise)), 201


if __name__ == '__main__':
    app.run(port=5555, debug=True)
#!/usr/bin/env python3

from datetime import date

from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
    print('Clearing existing data...')
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    print('Seeding exercises...')
    push_up = Exercise(name='Push Up', category='Strength', equipment_needed=False)
    squat = Exercise(name='Squat', category='Strength', equipment_needed=False)
    bench_press = Exercise(name='Bench Press', category='Strength', equipment_needed=True)
    running = Exercise(name='Running', category='Cardio', equipment_needed=False)
    plank = Exercise(name='Plank', category='Core', equipment_needed=False)

    db.session.add_all([push_up, squat, bench_press, running, plank])
    db.session.commit()

    print('Seeding workouts...')
    workout_1 = Workout(date=date(2026, 7, 20), duration_minutes=45, notes='Upper body day')
    workout_2 = Workout(date=date(2026, 7, 22), duration_minutes=30, notes='Cardio session')
    workout_3 = Workout(date=date(2026, 7, 25), duration_minutes=60, notes='Full body')

    db.session.add_all([workout_1, workout_2, workout_3])
    db.session.commit()

    print('Seeding workout_exercises...')
    workout_exercises = [
        WorkoutExercise(workout_id=workout_1.id, exercise_id=push_up.id, reps=15, sets=3),
        WorkoutExercise(workout_id=workout_1.id, exercise_id=bench_press.id, reps=10, sets=4),
        WorkoutExercise(workout_id=workout_2.id, exercise_id=running.id, duration_seconds=1800),
        WorkoutExercise(workout_id=workout_3.id, exercise_id=squat.id, reps=12, sets=3),
        WorkoutExercise(workout_id=workout_3.id, exercise_id=plank.id, duration_seconds=60),
    ]
    db.session.add_all(workout_exercises)
    db.session.commit()

    print('Seed complete!')
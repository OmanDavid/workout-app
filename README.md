# Workout Tracker API

## Description

A Flask + SQLAlchemy REST API backend for a workout tracking application used by personal trainers. The API tracks **Workouts** and reusable **Exercises**, connected through a **WorkoutExercise** join table that records reps, sets, and duration for each exercise performed in a given workout.

**Models & relationships**

- `Exercise` — has many `WorkoutExercise`s; has many `Workout`s through `WorkoutExercise`
- `Workout` — has many `WorkoutExercise`s; has many `Exercise`s through `WorkoutExercise`
- `WorkoutExercise` — belongs to a `Workout`; belongs to an `Exercise`

Data is validated at three levels: database table constraints, model-level validations (`@validates`), and Marshmallow schema validations on incoming request data.

## Installation

1. Clone the repository and move into the project folder.
2. Create and activate a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate # on Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Move into the `server/` directory:
   ```
   cd server
   ```
5. Initialize and apply the database migrations:
   ```
   flask db init
   flask db migrate -m "initial migration"
   flask db upgrade head
   ```
6. Seed the database with example data:
   ```
   python seed.py
   ```

## Running the app

From the `server/` directory:

```
flask run
```

or

```
python app.py
```

The API will be available at `http://127.0.0.1:5555`.

## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/workouts` | List all workouts |
| GET | `/workouts/<id>` | Show a single workout, including its associated exercises with reps/sets/duration |
| POST | `/workouts` | Create a workout (`date`, `duration_minutes`, `notes`) |
| DELETE | `/workouts/<id>` | Delete a workout and its associated `WorkoutExercise` records |
| GET | `/exercises` | List all exercises |
| GET | `/exercises/<id>` | Show a single exercise and the workouts it's used in |
| POST | `/exercises` | Create an exercise (`name`, `category`, `equipment_needed`) |
| DELETE | `/exercises/<id>` | Delete an exercise and its associated `WorkoutExercise` records |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout, including `reps`, `sets`, `duration_seconds` |

### Validations

- **Table constraints:** `duration_minutes > 0` on `Workout`; `reps >= 0` and `sets >= 0` on `WorkoutExercise`
- **Model validations:** non-empty `name`/`category` on `Exercise`, positive `duration_minutes` on `Workout`, non-negative `reps`/`sets` on `WorkoutExercise`
- **Schema validations:** required fields and range/length checks on all incoming POST data, returning `400` with descriptive error messages on failure

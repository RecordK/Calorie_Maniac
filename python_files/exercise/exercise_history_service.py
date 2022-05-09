from python_files.exercise.exercise_history_db import ExerciseHistoryDB
from python_files.exercise.exercise_history import ExerciseHistory

exercise_history_db = ExerciseHistoryDB()


class ExerciseHistoryService:

    def insert_data(self, exercise_index, exercise_name, start_time, end_time, exercised_time, use_kcal, count, coin):
        exercise_history_db.insert_exercise_data(exercise_index, exercise_name, start_time, use_kcal, count, coin)

    def retrieve_by_today(self):
        return exercise_history_db.select_by_date()

    def insert_start_by_index(self, exercise_index, exercise_name):
        exercise_history_db.insert_start_by_index(exercise_index, exercise_name)

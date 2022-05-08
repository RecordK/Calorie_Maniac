from python_files.exercise.exercise_history_db import ExerciseHistoryDB
from python_files.exercise.exercise_history import ExerciseHistory

exercise_history_db = ExerciseHistoryDB()
# exercise_history = ExerciseHistory()


class ExerciseHistoryService:

    def insert_data(self, exercise_index, exercise_name, start_time, end_time, exercised_time, use_kcal, count, coin):
        exercise_history_db.insert_data(exercise_index, exercise_name, start_time, end_time, exercised_time,
                                        use_kcal,
                                        count, coin)

    def retrieve_by_today(self):
        return exercise_history_db.select_by_date()

    def insert_start_by_index(self, exercise_index, exercise_name):
        exercise_history_db.insert_start_by_index(exercise_index, exercise_name)

    # def update_end_by_index(self, exercise_index, use_kcal, count):
    #     exercise_history_db.update_end_by_index(exercise_index, use_kcal, count)

    # def calc_exercised_time(self):
    #     exercised_time = exercise_history.end_time - exercise_history.start_time
    #     return exercised_time

    # def save_exercised_time(self, exercise_index):
    #     exercise_history_db.save_exercised_time(exercise_index)

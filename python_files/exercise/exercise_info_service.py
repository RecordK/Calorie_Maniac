from python_files.exercise.exercise_info_db import ExerciseInfoDB


class ExerciseInfoService:
    def __init__(self):
        self.exercise_db = ExerciseInfoDB()

    def retrieve_all(self):
        exercise_list = self.exercise_db.select_all()
        return exercise_list

    def retrieve_by_index(self, exercise_index):
        exercise_list = self.exercise_db.select_by_index(exercise_index)
        return exercise_list

    def retrieve_by_name(self, exercise_name):
        exercise_list = self.exercise_db.select_by_name(exercise_name)
        return exercise_list

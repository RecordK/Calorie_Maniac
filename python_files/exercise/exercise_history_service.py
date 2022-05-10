from python_files.exercise.exercise_history_db import ExerciseHistoryDB
from python_files.exercise.exercise_history import ExerciseHistory
from datetime import datetime, timedelta

exercise_history_db = ExerciseHistoryDB()


class ExerciseHistoryService:

    def insert_data(self, exercise_index, exercise_name, start_time, end_time, exercised_time, use_kcal, count, coin, month, week):
        exercise_history_db.insert_exercise_data(exercise_index, exercise_name, start_time, use_kcal, count, coin, month, week)

    def retrieve_by_today(self):
        return exercise_history_db.select_by_date()

    def retrieve_by_index(self, exercise_list):
        exercise_list = exercise_history_db.select_by_index(exercise_list)
        print(exercise_list)
        return exercise_list

    def insert_start_by_index(self, exercise_index, exercise_name):
        exercise_history_db.insert_start_by_index(exercise_index, exercise_name)

    def get_date(self, y, m, d):
        '''y: year(4 digits)
         m: month(2 digits)
         d: day(2 digits'''
        s = f'{y:04d}-{m:02d}-{d:02d}'
        return datetime.strptime(s, '%Y-%m-%d')

    def get_week_no(self, y, m, d):
        target = self.get_date(y, m, d)
        firstday = target.replace(day=1)
        if firstday.weekday() == 6:
            origin = firstday
        elif firstday.weekday() < 3:
            origin = firstday - timedelta(days=firstday.weekday() + 1)
        else:
            origin = firstday + timedelta(days=6-firstday.weekday())
        return (target - origin).days // 7 + 1
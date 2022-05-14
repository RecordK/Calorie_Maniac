from python_files.exercise.exercise_history_db import ExerciseHistoryDB
from python_files.exercise.exercise_history import ExerciseHistory
from datetime import datetime, timedelta

exercise_history_db = ExerciseHistoryDB()


class ExerciseHistoryService:

    def insert_data(self,
                    exercise_index, exercise_name, start_time,
                    end_time, exercised_time, use_kcal,
                    count, coin, month,
                    week, day, image):
        exercise_history_db.insert_exercise_data(
            exercise_index, exercise_name, start_time,
            use_kcal, count, coin,
            month, week, day,
            image
        )

    def retrieve_by_today(self):
        return exercise_history_db.select_by_date()

    def retrieve_by_index(self, exercise_list):
        exercise_list = exercise_history_db.select_by_index(exercise_list)
        print(exercise_list)
        return exercise_list

    def insert_start_by_index(self, exercise_index, exercise_name):
        exercise_history_db.insert_start_by_index(exercise_index, exercise_name)

    def get_date(self, y, m, d):
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
            origin = firstday + timedelta(days=6 - firstday.weekday())
        return (target - origin).days // 7 + 1

    def retrieve_by_month(self, month):
        exercise_month_list = exercise_history_db.select_by_month(month)
        return exercise_month_list

    def retrieve_by_week(self, week):
        exercise_week_list = exercise_history_db.select_by_week(week)
        return exercise_week_list

    def retrieve_by_day(self, day):
        exercise_day_list = exercise_history_db.select_by_day(day)
        return exercise_day_list

    def retrieve_coin(self):
        coin = exercise_history_db.select_sum_coin()
        return coin

    def retrieve_today_coin(self):
        today_coin = exercise_history_db.select_sum_coin_by_day()
        if today_coin is None:
            today_coin = 0
        return today_coin

from datetime import datetime, timedelta

from python_files.food.food_history_db import FoodHistoryDB
# from python_files.exercise.exercise_history_db import ExerciseHistoryDB

food_history_db = FoodHistoryDB()


class FoodHistoryService:
	def __init__(self):
		self.food_history_db = FoodHistoryDB()

	def insert_data(self, food_index, food_name, food_kcal, food_date, food_image, food_month, food_week):
		self.food_history_db.insert_data(food_index, food_name, food_kcal, food_date, food_image, food_month, food_week)

	def retrieve_by_index(self, food_index):
		food_list = food_history_db.select_by_index(food_index)
		print(food_list)
		return food_list

	def retrieve_by_today(self):
		return self.food_history_db.select_by_date()

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
		food_month_list = food_history_db.select_by_month(month)
		return food_month_list

	def retrieve_by_week(self, week):
		exercise_week_list = food_history_db.select_by_week(week)
		return exercise_week_list

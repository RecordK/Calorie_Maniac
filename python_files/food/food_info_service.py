from python_files.food.food_info_db import FoodInfoDB


class FoodInfoService:
	def __init__(self):
		self.food_db = FoodInfoDB()

	def insert_food(self, food_info):
		confirm = self.food_db.insert(food_info)
		return confirm

	def insert_foods(self):
		pass

	def find_food(self, food_name):
		exist_check = self.food_db.search_by_name(food_name)
		if exist_check is None:
			return 0
		else:
			return 1


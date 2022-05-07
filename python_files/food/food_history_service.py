from python_files.food.food_history_db import FoodHistoryDB


class FoodHistoryService:
	def __init__(self):
		self.food_history_db = FoodHistoryDB()

	def insert_data(self, food_index, food_name, food_image):
		self.food_history_db.insert_data(food_index, food_name, food_image)


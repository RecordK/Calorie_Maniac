import pandas as pd
from python_files.food.food_info import FoodInfo
from python_files.food.food_info_db import FoodInfoDB


class FoodInfoService:
	def __init__(self):
		self.food_db = FoodInfoDB()

	def insert_food(self, food_info):
		confirm = self.food_db.insert(food_info)
		return confirm

	def insert_foods(self, food_file, file_type):
		if file_type == 'csv':
			foods = pd.read_csv(food_file)
			foods = foods[['음 식 명', '에너지(kcal)', '탄수화물(g)', '단백질(g)', '지방(g)', '당류(g)']]
			foods_list = []
			for i in range(len(foods)):
				foods_list.append(
					[
						foods.iloc[i][0],
						foods.iloc[i][1],
						foods.iloc[i][2],
						foods.iloc[i][3],
						foods.iloc[i][4],
						foods.iloc[i][5],
					]
				)
			confirm = self.food_db.insert(foods_list)
			return confirm
		else:
			pass

		return 0

	def retrieve_all(self):
		food_list = self.food_db.select_all()
		return food_list

	def retrieve_by_index(self, food_index):
		food_list = self.food_db.select_by_index(food_index)
		return food_list

	def retrieve_by_name(self, food_name):
		food_list = self.food_db.select_by_name(food_name)
		return food_list

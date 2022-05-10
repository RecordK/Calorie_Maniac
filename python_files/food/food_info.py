class FoodInfo:
	def __init__(self, food_index=0, food_name=None, food_kcal=0, food_carbohydrate=0, food_protein=0, food_fat=0, food_sugars=0):
		self.food_index = food_index
		self.food_name = food_name
		self.food_kcal = food_kcal
		self.food_carbohydrate = food_carbohydrate
		self.food_protein = food_protein
		self.food_fat = food_fat
		self.food_sugars = food_sugars

	def __str__(self):
		return self.food_name, self.food_kcal, self.food_carbohydrate, self.food_protein, self.food_fat, self.food_sugars





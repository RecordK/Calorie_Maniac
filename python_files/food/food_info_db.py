import logging
import pymysql
from python_files.food.food_info import FoodInfo


# local mysql!!!
class FoodInfoDB:
	logger = logging.getLogger()

	def __init__(self):
		self.conn = None

	def connection(self):
		self.conn = pymysql.connect(host='localhost', user='root', password='1234', db='calorieManiac')

	def disconnection(self):
		self.conn.close()

	def insert(self, food_info: FoodInfo):
		try:
			self.connection()
			cursor = self.conn.cursor()
			if isinstance(food_info, list):
				sql = 'INSERT INTO food_info(food_name, food_kcal, food_carbohydrate, food_protein, food_fat, food_sugars) VALUES'\
						+', '.join('(%s, %s, %s, %s, %s, %s)' for _ in food_info)
				flatten_values = [food for food_info_list in food_info for food in food_info_list]
				cursor.execute(sql, flatten_values)
			else:
				sql = 'INSERT INTO food_info(food_name, food_kcal, food_carbohydrate, food_protein, food_fat, food_sugars) VALUES (%s, %s, %s, %s, %s, %s)'
				data = (food_info.food_name, food_info.food_kcal, food_info.food_carbohydrate, food_info.food_protein, food_info.food_fat, food_info.food_sugars)
				cursor.execute(sql, data)
			self.conn.commit()
			return True
		except Exception as e:
			self.logger.error(e)
			return False
		finally:
			self.disconnection()

	def select_all(self):
		try:
			self.connection()
			cursor = self.conn.cursor()
			sql = 'SELECT * FROM food_info'
			cursor.execute(sql, )
			foods = []
			for row in cursor:
				foods.append(FoodInfo(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
			return foods
		except Exception as e:
			self.logger.error(e)
		finally:
			self.disconnection()

	def select_by_name(self, name):
		try:
			self.connection()
			cursor = self.conn.cursor()
			sql = 'SELECT * FROM food_info WHERE food_name LIKE %s'
			data = (name, )
			cursor.execute(sql, data)
			foods = []
			for row in cursor:
				foods.append(FoodInfo(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
			return foods
		except Exception as e:
			self.logger.error(e)
		finally:
			self.disconnection()


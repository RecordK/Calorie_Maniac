import logging
import pymysql
from python_files.food.food_history import FoodHistory


class FoodHistoryDB:
	logger = logging.getLogger()

	def __init__(self):
		self.conn = None

	def connection(self):
		self.conn = pymysql.connect(host='localhost', user='root', password='1234', db='calorieManiac')

	def disconnection(self):
		self.conn.close()

	def select_by_index(self):
		pass

	def insert_by_food_index(self):
		try:
			self.connection()
			cursor = self.conn.cursor()
			sql = 'INSERT INTO food_history(food_index, food_name, food_data, food_image) VALUES (%s, %s, %s, %s)'

		except Exception as e:
			self.logger.error(e)
		finally:
			self.disconnection()

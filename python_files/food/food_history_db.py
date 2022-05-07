import logging
import pymysql
from _datetime import datetime
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

	def insert_data(self, food_index, food_name, food_image):
		try:
			self.connection()
			cursor = self.conn.cursor()
			if food_image is None:
				sql = 'INSERT INTO food_history(food_index, food_name) VALUES (%s, %s)'
				data = (int(food_index), food_name)
				cursor.execute(sql, data)
			self.conn.commit()
			return True
		except Exception as e:
			self.logger.error(e)
		finally:
			self.disconnection()

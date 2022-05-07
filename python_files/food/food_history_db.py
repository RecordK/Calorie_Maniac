import logging
import pymysql
from python_files.food.food_history import FoodHistory
from _datetime import datetime
from python_files.setting.db_setting import DBSetting


class FoodHistoryDB:
	logger = logging.getLogger()

	def __init__(self):
		self.conn = None
		self.host = DBSetting.HOST
		self.user = DBSetting.USER
		self.password = DBSetting.PASSWORD
		self.db_schema = DBSetting.DBSCHEMA

	def connection(self):
		self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db_schema)

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
			else:			# not test
				sql = 'INSERT INTO food_history(food_index, food_name, food_image) VALUES (%s, %s, %s)'
				data = (int(food_index), food_name, food_image)
			cursor.execute(sql, data)
			self.conn.commit()
			return True
		except Exception as e:
			self.logger.error(e)
		finally:
			self.disconnection()

	def select_by_date(self):		# not test
		try:
			self.connection()
			cursor = self.conn.cursor()
			today = datetime.today().strftime("%Y-%m-%d")
			sql = 'SELECT * FROM food_history WHERE DATE(food_date) = %s'
			date = (today, )
			cursor.execute(sql, date)
			food_today = []
			for row in cursor:
				food_today.append(FoodHistory(row[1], row[2], row[3], row[4]))
			return food_today
		except Exception as e:
			self.logger.error(e)
		finally:
			self.disconnection()

import logging
import pymysql
from python_files.food.food_history import FoodHistory
from datetime import datetime
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

	def insert_data(self, food_index, food_name, food_kcal, food_date, food_image, food_month, food_week, food_day):
		try:
			self.connection()
			cursor = self.conn.cursor()
			sql = 'INSERT INTO food_history(food_index, food_name, food_kcal, food_date, food_image, food_month, food_week, food_day) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
			data = (int(food_index), food_name, food_kcal, food_date, food_image, food_month, food_week, food_day)
			cursor.execute(sql, data)
			self.conn.commit()
			return True
		except Exception as e:
			self.logger.error(e)
		finally:
			self.disconnection()

	def select_by_date(self):
		try:
			self.connection()
			cursor = self.conn.cursor()
			today = datetime.today().strftime("%Y-%m-%d")
			print('food_history_db-today:', today)
			sql = 'SELECT * FROM food_history WHERE DATE(food_date) = %s'
			date = (today, )
			cursor.execute(sql, date)
			food_today = []
			for row in cursor:
				food_today.append(FoodHistory(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
			print('food_history_db-food_toady[]:', food_today)
			return food_today
		except Exception as e:
			self.logger.error(e)
		finally:
			self.disconnection()

	def select_by_month(self, month):

		try:
			self.connection()
			cursor = self.conn.cursor()
			sql = 'SELECT * FROM food_history WHERE food_month = %s'
			date = (month,)
			cursor.execute(sql, date)
			food_today = []
			for row in cursor:
				food_today.append(
					FoodHistory(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
			return food_today
		except Exception as e:
			self.logger.error(e)
		finally:
			self.disconnection()

	def select_by_week(self, week):

		try:
			self.connection()
			cursor = self.conn.cursor()
			sql = 'SELECT * FROM food_history WHERE food_week = %s'
			date = (week,)
			cursor.execute(sql, date)
			food_today = []
			for row in cursor:
				food_today.append(
					FoodHistory(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
			return food_today
		except Exception as e:
			self.logger.error(e)
		finally:
			self.disconnection()

	def select_by_day(self, day):

		try:
			self.connection()
			cursor = self.conn.cursor()
			sql = 'SELECT * FROM food_history WHERE food_day = %s'
			date = (day,)
			cursor.execute(sql, date)
			food_today = []
			for row in cursor:
				food_today.append(
					FoodHistory(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
			return food_today
		except Exception as e:
			self.logger.error(e)
		finally:
			self.disconnection()

	def select_by_index(self, food_index):
		try:
			self.connection()
			cursor = self.conn.cursor()
			if isinstance(food_index, list):
				sql = 'SELECT * FROM food_history WHERE food_index IN (' + ', '.join(
					('%s') for _ in food_index) + ')'
				cursor.execute(sql, food_index)
				food_list = []
				for row in cursor:
					food_list.append(
						FoodHistory(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
				return food_list
			else:
				sql = 'SELECT * FROM food_history WHERE food_index = (%s)'
				index = int(food_index)
				data = (index,)
				cursor.execute(sql, data)
				row = cursor.fetchone()
				return FoodHistory(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
		except Exception as e:
			self.logger.error(e)
		finally:
			self.disconnection()

	def select_food_join_all(self, today):
		try:
			self.connection()
			cursor = self.conn.cursor()
			sql = 'SELECT * FROM food_history LEFT JOIN food_info fi ON fi.food_index = food_history.food_index WHERE DATE (food_date) = %s ORDER BY food_date DESC'
			cursor.execute(sql, (today, ))
			food_all = []
			if cursor is None:
				return food_all
			else:
				for row in cursor:
					food_all.append([row[9], row[2], row[4], row[5], row[11], row[12], row[13], row[14], row[15]])
				print('food:', food_all)
				return food_all
		except Exception as e:
			self.logger.error(e)
		finally:
			self.disconnection()


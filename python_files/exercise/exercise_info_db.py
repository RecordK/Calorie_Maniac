import logging
import pymysql
from Calorie_Maniac.python_files.exercise.exercise_info import ExerciseInfo


# local mysql!!!
class ExerciseInfoDB:
	logger = logging.getLogger()

	def __init__(self):
		self.conn = None

	def connection(self):
		self.conn = pymysql.connect(host='localhost', user='root', password='1234', db='calorieManiac')

	def disconnection(self):
		self.conn.close()

	def insert(self, exercise_info: ExerciseInfo):
		try:
			self.connection()
			cursor = self.conn.cursor()
			if isinstance(exercise_info, list):
				sql = 'INSERT INTO exercise_info(exercise_name, exercise_use_kcal, exercise_img) VALUES'\
						+', '.join('(%s, %s, %s)' for _ in exercise_info)
				flatten_values = [exercise for exercise_info_list in exercise_info for exercise in exercise_info_list]
				cursor.execute(sql, flatten_values)
			else:
				sql = 'INSERT INTO exercise_info(exercise_name, exercise_use_kcal, exercise_img) VALUES (%s, %s, %s, %s, %s, %s)'
				data = (exercise_info.exercise_name, exercise_info.exercise_use_kcal, exercise_info.exercise_img)
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
			sql = 'SELECT * FROM exercise_info'
			cursor.execute(sql, )
			foods = []
			for row in cursor:
				foods.append(ExerciseInfo(row[0], row[1], row[2], row[3]))
			return foods
		except Exception as e:
			self.logger.error(e)
		finally:
			self.disconnection()

	def select_by_name(self, name):
		try:
			self.connection()
			cursor = self.conn.cursor()
			sql = 'SELECT * FROM exercise_info WHERE exercise_name LIKE %s'
			data = (name, )
			cursor.execute(sql, data)
			exercises = []
			for row in cursor:
				exercises.append(ExerciseInfo(row[0], row[1], row[2], row[3]))
			return exercises
		except Exception as e:
			self.logger.error(e)
		finally:
			self.disconnection()


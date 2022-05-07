import logging
import pymysql
from python_files.exercise.exercise_info import ExerciseInfo


# local mysql!!!
class ExerciseInfoDB:
    logger = logging.getLogger()

    def __init__(self):
        self.conn = None

    def connection(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='1234', db='calorieManiac')

    def disconnection(self):
        self.conn.close()

    def select_all(self):
        try:
            self.connection()
            cursor = self.conn.cursor()
            sql = 'SELECT * FROM exercise_info'
            cursor.execute(sql, )
            exercises = []
            for row in cursor:
                exercises.append(ExerciseInfo(row[0], row[1], row[2]))
            return exercises
        except Exception as e:
            self.logger.error(e)
        finally:
            self.disconnection()

    def select_by_index(self, exercise_index):
        try:
            self.connection()
            cursor = self.conn.cursor()
            sql = 'SELECT * FROM exercise_info WHERE exercise_index = %s'
            data = (int(exercise_index),)
            cursor.execute(sql, data)
            exercises = []
            for row in cursor:
                exercises.append(ExerciseInfo(row[0], row[1], row[2]))
            return exercises
        except Exception as e:
            self.logger.error(e)
        finally:
            self.disconnection()

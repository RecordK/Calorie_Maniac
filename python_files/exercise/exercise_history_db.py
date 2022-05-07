import logging
import pymysql
from python_files.exercise.exercise_history import ExerciseHistory


class ExerciseHistoryDB:
    logger = logging.getLogger()

    def __init__(self):
        self.conn = None

    def connection(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='', db='calorieManiac')

    def disconnection(self):
        self.conn.close()

    def select_by_index(self):
        pass

    def insert_by_exercise_index(self):
        try:
            self.connection()
            cursor = self.conn.cursor()
            sql = 'INSERT INTO exec_history(exercise_index, exercise_name, start_time, end_time, exercised_time, use_kcal, count, coin) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'

        except Exception as e:
            self.logger.error(e)
        finally:
            self.disconnection()

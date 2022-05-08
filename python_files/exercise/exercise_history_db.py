import logging
import pymysql
from python_files.exercise.exercise_history import ExerciseHistory
from _datetime import datetime
from python_files.setting.db_setting import DBSetting


class ExerciseHistoryDB:
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

    def insert_data(self, exercise_index, exercise_name, start_time, end_time, exercised_time, use_kcal, count, coin):
        try:
            self.connection()
            cursor = self.conn.cursor()
            sql = 'INSERT INTO exercise_history(exercise_index, exercise_name, start_time, end_time, exercised_time, use_kcal, count, coin) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
            data = (exercise_index, exercise_name, start_time, end_time, exercised_time, use_kcal, count, coin)
            cursor.execute(sql, data)
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.error(e)
        finally:
            self.disconnection()

    def select_by_date(self):  # not test

        try:
            self.connection()
            cursor = self.conn.cursor()
            today = datetime.today().strftime("%Y-%m-%d")
            sql = 'SELECT * FROM exercise_history WHERE DATE(end_time) = %s'
            date = (today,)
            cursor.execute(sql, date)
            exercise_today = []
            for row in cursor:
                exercise_today.append(ExerciseHistory(row[1], row[2], row[4], row[5], row[6], row[7], row[8]))
            return exercise_today
        except Exception as e:
            self.logger.error(e)
        finally:
            self.disconnection()

    def insert_start_by_index(self, exercise_index, exercise_name):

        try:
            self.connection()
            cursor = self.conn.cursor()
            start_time = datetime.now()
            sql = 'INSERT INTO exercise_history(exercise_index, exercise_name, start_time) VALUES (%s, %s, %s)'
            data = (exercise_index, exercise_name, start_time)
            cursor.execute(sql, data)
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.error(e)
        finally:
            self.disconnection()

    def update_end_by_index(self, exercise_index, use_kcal, count):
        try:
            self.connection()
            cursor = self.conn.cursor()
            end_time = datetime.now()
            sql = 'UPDATE exercise_history SET end_time = %s, use_kcal = %s, count = %s WHERE exercise_index = %s'
            data = (end_time, use_kcal, count, exercise_index)
            cursor.execute(sql, data)
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.error(e)
        finally:
            self.disconnection()

    def insert_end_by_index(self, exercise_index, use_kcal, count):
        try:
            self.connection()
            cursor = self.conn.cursor()
            end_time = datetime.now()
            sql = 'INSERT INTO exercise_history (end_time, use_kcal, count) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE use_kcal = VALUE(use_kcal) + use_kcal, count = VALUE(count) +count WHERE exercise_index = %s'
            data = (end_time, use_kcal, count, exercise_index)
            cursor.execute(sql, data)
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.error(e)
        finally:
            self.disconnection()

    def select_time(self, exercise_index):
        try:
            self.connection()
            cursor = self.conn.cursor()
            sql = 'SELECT start_time, end_time FROM exercise_history WHERE exercise_index = %s'
            time = (exercise_index,)
            cursor.execute(sql, time)
            exercise_time = []
            for row in cursor:
                exercise_time.append(ExerciseHistory(row[1], row[3], row[4]))
            return exercise_time
        except Exception as e:
            self.logger.error(e)
        finally:
            self.disconnection()

    def save_exercised_time(self, exercise_index):
        try:
            self.connection()
            cursor = self.conn.cursor()
            exec_time = self.select_time(exercise_index)[1] - self.select_time(exercise_index)[2]
            sql = 'UPDATE exercise_history SET exercised_time = %s WHERE exercise_index = %s'
            data = (exec_time, exercise_index)
            cursor.execute(sql, data)
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.error(e)
        finally:
            self.disconnection()

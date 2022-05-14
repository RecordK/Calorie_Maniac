import logging
import pymysql
from python_files.exercise.exercise_history import ExerciseHistory
from datetime import datetime
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

    def select_by_index(self, exercise_list):
        try:
            self.connection()
            cursor = self.conn.cursor()
            if isinstance(exercise_list, list):
                sql = 'SELECT * FROM exercise_history WHERE exercise_list IN (' + ', '.join(
                    ('%s') for _ in exercise_list) + ')'
                cursor.execute(sql, exercise_list)
                exercise_list = []
                for row in cursor:
                    exercise_list.append(
                        ExerciseHistory(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                                        row[10], row[11], row[12]))
                return exercise_list
            else:
                sql = 'SELECT * FROM exercise_history WHERE exercise_list = (%s)'
                exercise_list = int(exercise_list)
                data = (exercise_list,)
                cursor.execute(sql, data)
                row = cursor.fetchone()
                return ExerciseHistory(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                                       row[10], row[11], row[12])
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
                exercise_today.append(
                    ExerciseHistory(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                                    row[10], row[11], row[12]))
            return exercise_today
        except Exception as e:
            self.logger.error(e)
        finally:
            self.disconnection()

    def insert_exercise_data(self, exercise_index, exercise_name, start_time, end_time, exercised_time, use_kcal, count,
                             coin, month, week, day, image):
        try:
            self.connection()
            cursor = self.conn.cursor()
            sql = 'INSERT INTO exercise_history (' \
                  'exercise_index, exercise_name, start_time, end_time, exercised_time, use_kcal, count, coin, month, week, day, image' \
                  ') VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            data = (
            exercise_index, exercise_name, start_time, end_time, exercised_time, use_kcal, count, coin, month, week, day, image)
            cursor.execute(sql, data)
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.error(e)
        finally:
            self.disconnection()

    def select_by_month(self, month):

        try:
            self.connection()
            cursor = self.conn.cursor()
            sql = 'SELECT * FROM exercise_history WHERE month = %s'
            date = (month,)
            cursor.execute(sql, date)
            exercise_today = []
            for row in cursor:
                exercise_today.append(
                    ExerciseHistory(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                                    row[10], row[11], row[12]))
            return exercise_today
        except Exception as e:
            self.logger.error(e)
        finally:
            self.disconnection()

    def select_by_week(self, week):

        try:
            self.connection()
            cursor = self.conn.cursor()
            sql = 'SELECT * FROM exercise_history WHERE week = %s'
            date = (week,)
            cursor.execute(sql, date)
            exercise_today = []
            for row in cursor:
                exercise_today.append(
                    ExerciseHistory(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                                    row[10], row[11], row[12]))
            return exercise_today
        except Exception as e:
            self.logger.error(e)
        finally:
            self.disconnection()

    def select_by_day(self, day):

        try:
            self.connection()
            cursor = self.conn.cursor()
            sql = 'SELECT * FROM exercise_history WHERE day = %s'
            date = (day,)
            cursor.execute(sql, date)
            exercise_today = []
            for row in cursor:
                exercise_today.append(
                    ExerciseHistory(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                                    row[10], row[11], row[12]))
            return exercise_today
        except Exception as e:
            self.logger.error(e)
        finally:
            self.disconnection()

    def select_sum_coin(self):
        try:
            self.connection()
            cursor = self.conn.cursor()
            sql = 'SELECT sum(coin) from exercise_history'
            cursor.execute(sql)
            coin = cursor.fetchone()
            return coin[0]
        except Exception as e:
            self.logger.error(e)
        finally:
            self.disconnection()

    def select_sum_coin_by_day(self):
        try:
            self.connection()
            cursor = self.conn.cursor()
            today = datetime.today().strftime("%Y-%m-%d")
            sql = 'SELECT sum(coin) from exercise_history WHERE DATE(end_time) = %s'
            cursor.execute(sql, today)
            coin = cursor.fetchone()
            return coin[0]
        except Exception as e:
            self.logger.error(e)
        finally:
            self.disconnection()

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

    def select_by_index(self, exercise_index):
        try:
            self.connection()
            cursor = self.conn.cursor()
            if isinstance(exercise_index, list):
                sql = 'SELECT * FROM exercise_history WHERE exercise_index IN (' + ', '.join(('%s') for _ in exercise_index) + ')'
                cursor.execute(sql, exercise_index)
                exercise_list = []
                for row in cursor:
                    exercise_list.append(ExerciseHistory(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
                return exercise_list
            else:
                sql = 'SELECT * FROM exercise_history WHERE exercise_index = (%s)'
                index = int(exercise_index)
                data = (index,)
                cursor.execute(sql, data)
                row = cursor.fetchone()
                return ExerciseHistory(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
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
                exercise_today.append(ExerciseHistory(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
            return exercise_today
        except Exception as e:
            self.logger.error(e)
        finally:
            self.disconnection()

    def insert_exercise_data(self, exercise_index, exercise_name, start_time, end_time, exercised_time, use_kcal, count,
                             coin):
        try:
            self.connection()
            cursor = self.conn.cursor()
            sql = 'INSERT INTO exercise_history (exercise_index, exercise_name, start_time, end_time, exercised_time, use_kcal, count, coin) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
            data = (exercise_index, exercise_name, start_time, end_time, exercised_time, use_kcal, count, coin)
            cursor.execute(sql, data)
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.error(e)
        finally:
            self.disconnection()

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

    def select_by_index(self, exercise_list):
        try:
            self.connection()
            cursor = self.conn.cursor()
            if isinstance(exercise_list, list):
                sql = 'SELECT * FROM exercise_history WHERE exercise_list IN (' + ', '.join(('%s') for _ in exercise_list) + ')'
                print(sql)
                cursor.execute(sql, exercise_list)
                exercise_list = []
                for row in cursor:
                    exercise_list.append(ExerciseHistory(row[0],row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]))
                    print(exercise_list)
                return exercise_list
            else:
                sql = 'SELECT * FROM exercise_history WHERE exercise_list = (%s)'
                exercise_list = int(exercise_list)
                data = (exercise_list,)
                cursor.execute(sql, data)
                row = cursor.fetchone()
                return ExerciseHistory(row[0],row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
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
                exercise_today.append(ExerciseHistory(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]))
            return exercise_today
        except Exception as e:
            self.logger.error(e)
        finally:
            self.disconnection()

    def insert_exercise_data(self, exercise_index, exercise_name, start_time, end_time, exercised_time, use_kcal, count,
                             coin, month, week):
        try:
            self.connection()
            cursor = self.conn.cursor()
            sql = 'INSERT INTO exercise_history (exercise_index, exercise_name, start_time, end_time, exercised_time, use_kcal, count, coin, month, week) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            data = (exercise_index, exercise_name, start_time, end_time, exercised_time, use_kcal, count, coin, month, week)
            cursor.execute(sql, data)
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.error(e)
        finally:
            self.disconnection()

    # def sum_kcal_data(self, exercise_list):
    #     # 1~7: 1주차
    #     # 8~14: 2주차
    #     # 15~21: 3주차
    #     # 22~ :4주차
    #     try:
    #         self.connection()
    #         cursor = self.conn.cursor()
    #         if isinstance(exercise_list, list):
    #             sql = 'SELECT use_kcal FROM exercise_history WHERE exercise_list IN (' + ', '.join(
    #                 ('%s') for _ in exercise_list) + ')'
    #             print(sql)
    #             cursor.execute(sql, exercise_list)
    #             exercise_list = []
    #             for row in cursor:
    #                 exercise_list.append(
    #                     ExerciseHistory(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
    #                 print(exercise_list)
    #             return exercise_list
    #         else:
    #             sql = 'SELECT * FROM exercise_history WHERE exercise_list = (%s)'
    #             exercise_list = int(exercise_list)
    #             data = (exercise_list,)
    #             cursor.execute(sql, data)
    #             row = cursor.fetchone()
    #             return ExerciseHistory(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
    #     except Exception as e:
    #         self.logger.error(e)
    #     finally:
    #         self.disconnection()

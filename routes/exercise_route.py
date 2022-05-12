from dateutil.utils import today
from flask import Blueprint, Flask, render_template, request, session, Response
from datetime import datetime
import glob

# from python_files.exercise import exercise_history_service
from python_files.exercise.exercise_history_service import ExerciseHistoryService
from python_files.exercise.exercise_info_db import ExerciseInfoDB
from python_files.exercise.exec_service import Exersize_service
from python_files.exercise.exercise_history_db import ExerciseHistoryDB

bp = Blueprint('health', __name__, url_prefix='/main/health')

execdb = ExerciseInfoDB()
execserv = Exersize_service()
exechistorydb = ExerciseHistoryDB()
exercise_history_service = ExerciseHistoryService()


@bp.get('/')
def main():
    exercise_list = [
        ['1.png', '푸쉬업'],
        ['2.png', '스쿼트'],
        ['3.png', '크런치'],
        ['4.png', '라잉레그레이즈'],
        ['5.png', '딥스'],
        ['6.png', '암컬'],
        ['7.png', '런지'],
        ['8.png', '풀업'],
        ['9.png', '사이드 레터럴 레이즈']
    ]
    return render_template('exercise_page.html', exercise_list=exercise_list)


@bp.get('/realtime')
def move_page():
    req_index = request.args.get('index')
    data_index = execdb.select_by_index(req_index)
    idx = data_index[0].exercise_index
    name = data_index[0].exercise_name

    # check
    print(idx)
    print(name)
    start_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    return render_template('realtime.html', index=idx, name=name, start_time=start_time)


@bp.post('/exercise_result/')
def exercise_result():
    st_time = request.form['start_exec']
    index = request.form['index_exec']
    data_index = execdb.select_by_index(index)
    idx = data_index[0].exercise_index
    name = data_index[0].exercise_name
    counter = execserv.counter
    calories = execserv.calories
    coin = execserv.coin
    start_time = datetime.strptime(st_time, "%Y-%m-%d %H:%M:%S")
    ed_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime(ed_time, "%Y-%m-%d %H:%M:%S")
    exercised_time = round((lambda x, y: y - x)(start_time, end_time).total_seconds())
    end_date = datetime.today().strftime("%Y-%m-%d")
    y = int(end_date.split('-')[0])
    m = int(end_date.split('-')[1])
    d = int(end_date.split('-')[2])
    week = exercise_history_service.get_week_no(y, m, d)
    month = datetime.today().strftime("%m")
    day = datetime.today().strftime("%d")

    print('idx type: ', type(idx))
    exercise_image = 'images/exercise_img/' + idx + '.png'  # 이미지 없을때 기본 경로

    # insert data in sql
    exechistorydb.insert_exercise_data(idx, name, start_time, end_time, exercised_time, calories, counter, coin, month,
                                       week, day, exercise_image)
    return render_template('index.html', name=name, start_time=start_time, end_time=end_time,
                           exercised_time=exercised_time, counter=counter, calories=calories, coin=coin, month=month,
                           week=week, day=day, exercise_image=exercise_image)


@bp.route('/video_feed_arm_curl')
def video_feed_arm_curl():
    return Response(execserv.arm_curl(), mimetype='multipart/x-mixed-replace; boundary=frame')


@bp.route('/video_feed_chair_dips')
def video_feed_chair_dips():
    return Response(execserv.chair_dips(), mimetype='multipart/x-mixed-replace; boundary=frame')


@bp.route('/video_feed_crunch')
def video_feed_crunch():
    return Response(execserv.crunch(), mimetype='multipart/x-mixed-replace; boundary=frame')


@bp.route('/video_feed_leg_raise')
def video_feed_leg_raise():
    return Response(execserv.leg_raise(), mimetype='multipart/x-mixed-replace; boundary=frame')


@bp.route('/video_feed_lunge')
def video_feed_lunge():
    return Response(execserv.lunge(), mimetype='multipart/x-mixed-replace; boundary=frame')


@bp.route('/video_feed_pull_up')
def video_feed_pull_up():
    return Response(execserv.pull_up(), mimetype='multipart/x-mixed-replace; boundary=frame')


@bp.route('/video_feed_push_up')
def video_feed_push_up():
    return Response(execserv.push_up(), mimetype='multipart/x-mixed-replace; boundary=frame')


@bp.route('/video_feed_side_lateral_raise')
def video_feed_side_lateral_raise():
    return Response(execserv.side_lateral_raise(), mimetype='multipart/x-mixed-replace; boundary=frame')


@bp.route('/video_feed_squat')
def video_feed_squat():
    return Response(execserv.squat(), mimetype='multipart/x-mixed-replace; boundary=frame')

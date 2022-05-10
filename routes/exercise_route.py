from dateutil.utils import today
from flask import Blueprint, Flask, render_template, request, session, Response
from datetime import datetime
import glob

from python_files.exercise.exercise_info_db import ExerciseInfoDB
from python_files.exercise.exec_service import Exersize_service
from python_files.exercise.exercise_history_db import ExerciseHistoryDB

bp = Blueprint('health', __name__, url_prefix='/main/health')




@bp.get('/')
def main():
    exercise_list = [
        ['push_up.png', '푸쉬업'],
        ['squat.png', '스쿼트'],
        ['crunch.png', '크런치'],
        ['lying_reg_raise.png', '라잉레그레이즈'],
        ['dips.png', '딥스'],
        ['arm_curl.png', '암컬'],
        ['cross_lunge.png', '런지'],
        ['pull_up.png', '풀업'],
        ['side_lateral_raise.png', '사이드 레터럴 레이즈']
    ]
    return render_template('exercise_page.html', exercise_list=exercise_list)


@bp.get('/realtime')
def move_page():
    execdb = ExerciseInfoDB()
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
    execdb = ExerciseInfoDB()
    execserv = Exersize_service()
    exechistorydb = ExerciseHistoryDB()
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

    # check
    print('index: ', index)
    print('name:', name)
    print('counter: ', counter)
    print('calories: ', calories)
    print('coins: ', coin)
    print('start_time: ', start_time)
    print('end_time: ', end_time)
    print('exercised_time: ', exercised_time)

    # insert data in sql
    exechistorydb.insert_exercise_data(idx, name, start_time, end_time, exercised_time, calories, counter, coin)
    return render_template('index.html', name=name, start_time=start_time, end_time=end_time,
                           exercised_time=exercised_time, counter=counter, calories=calories, coin=coin)


@bp.route('/video_feed_arm_curl')
def video_feed_arm_curl():
    execserv = Exersize_service()
    return Response(execserv.arm_curl(), mimetype='multipart/x-mixed-replace; boundary=frame')


@bp.route('/video_feed_chair_dips')
def video_feed_chair_dips():
    execserv = Exersize_service()
    return Response(execserv.chair_dips(), mimetype='multipart/x-mixed-replace; boundary=frame')


@bp.route('/video_feed_crunch')
def video_feed_crunch():
    execserv = Exersize_service()
    return Response(execserv.crunch(), mimetype='multipart/x-mixed-replace; boundary=frame')


@bp.route('/video_feed_leg_raise')
def video_feed_leg_raise():
    execserv = Exersize_service()
    return Response(execserv.leg_raise(), mimetype='multipart/x-mixed-replace; boundary=frame')


@bp.route('/video_feed_lunge')
def video_feed_lunge():
    execserv = Exersize_service()
    return Response(execserv.lunge(), mimetype='multipart/x-mixed-replace; boundary=frame')


@bp.route('/video_feed_pull_up')
def video_feed_pull_up():
    execserv = Exersize_service()
    return Response(execserv.pull_up(), mimetype='multipart/x-mixed-replace; boundary=frame')


@bp.route('/video_feed_push_up')
def video_feed_push_up():
    execserv = Exersize_service()
    return Response(execserv.push_up(), mimetype='multipart/x-mixed-replace; boundary=frame')


@bp.route('/video_feed_side_lateral_raise')
def video_feed_side_lateral_raise():
    execserv = Exersize_service()
    return Response(execserv.side_lateral_raise(), mimetype='multipart/x-mixed-replace; boundary=frame')


@bp.route('/video_feed_squat')
def video_feed_squat():
    execserv = Exersize_service()
    return Response(execserv.squat(), mimetype='multipart/x-mixed-replace; boundary=frame')

from flask import Blueprint, Flask, render_template, request, session, Response
from datetime import datetime
import glob
from python_files.exercise.exercise_info_db import ExerciseInfoDB
from python_files.exercise.exec_service import Exersize_service
from python_files.exercise.exercise_history_db import ExerciseHistoryDB
from python_files.exercise.exercise_history_service import ExerciseHistoryService

bp = Blueprint('health', __name__, url_prefix='/main/health')

execdb = ExerciseInfoDB()
execserv = Exersize_service()
exechistorydb = ExerciseHistoryDB()
exechistoryserv = ExerciseHistoryService()


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
    req_index = request.args.get('index')
    data_index = execdb.select_by_index(req_index)
    print(data_index[0].exercise_index)
    idx = data_index[0].exercise_index
    name = data_index[0].exercise_name
    print(name)
    exechistoryserv.insert_start_by_index(idx, name)
    return render_template('realtime.html', index=idx, name=name)


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


@bp.route('/exercise_result/<int:index>')
def exercise_result(index):
    print('exec_index: ', index)
    data_index = execdb.select_by_index(index)
    idx = data_index[0].exercise_index
    name = data_index[0].exercise_name
    print('name:', name)
    counter = execserv.counter
    print('counter: ', counter)
    calories = execserv.calories
    print('calories: ', calories)
    exechistorydb.update_end_by_index(idx, calories, counter)
    # exechistorydb.save_exercised_time(idx)
    return render_template('exercise_result.html', name=name, counter=counter, calories=calories)

from flask import Blueprint, Flask, render_template, request, session, Response
from datetime import datetime
import glob

bp = Blueprint('health', __name__, url_prefix='/main/health')


@bp.get('/')
def main():
    exercise_list = [
        ['push_up.png', '푸쉬업'],
        ['squat.png', '스쿼트'],
        ['crunch.png', '크런치'],
        ['lying_reg_raise.png', '라잉 레그 레이즈'],
        ['dips.png', '딥스'],
        ['bicycle_crunch.png', '바이시클 크런치'],
        ['cross_lunge.png', '크로스 런지'],
        ['pull_up.png', '폴업'],
        ['side_lateral_raise.png', '사이드 레터럴 레이즈']
    ]
    return render_template('exercise_page.html', exercise_list=exercise_list)


@bp.get('/realtime')
def move_page():
    index = request.args.get('index')
    print(index)
    return index


@bp.route('/video_feed_arm_curl')
def video_feed_arm_curl():
    return Response(exec.arm_curl(), mimetype='multipart/x-mixed-replace; boundary=frame')


@bp.route('/video_feed_chair_dips')
def video_feed_chair_dips():
    return Response(exec.chair_dips(), mimetype='multipart/x-mixed-replace; boundary=frame')


@bp.route('/video_feed_crunch')
def video_feed_crunch():
    return Response(exec.crunch(), mimetype='multipart/x-mixed-replace; boundary=frame')


@bp.route('/video_feed_leg_raise')
def video_feed_leg_raise():
    return Response(exec.leg_raise(), mimetype='multipart/x-mixed-replace; boundary=frame')


@bp.route('/video_feed_lunge')
def video_feed_lunge():
    return Response(exec.lunge(), mimetype='multipart/x-mixed-replace; boundary=frame')


@bp.route('/video_feed_pull_up')
def video_feed_pull_up():
    return Response(exec.pull_up(), mimetype='multipart/x-mixed-replace; boundary=frame')


@bp.route('/video_feed_push_up')
def video_feed_push_up():
    return Response(exec.push_up(), mimetype='multipart/x-mixed-replace; boundary=frame')


@bp.route('/video_feed_side_lateral_raise')
def video_feed_side_lateral_raise():
    return Response(exec.side_lateral_raise(), mimetype='multipart/x-mixed-replace; boundary=frame')


@bp.route('/video_feed_squat')
def video_feed_squat():
    return Response(exec.squat(), mimetype='multipart/x-mixed-replace; boundary=frame')

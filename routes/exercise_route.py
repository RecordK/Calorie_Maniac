from flask import Blueprint, Flask, render_template, request, session
from datetime import datetime
import glob

bp = Blueprint('health', __name__, url_prefix='/main/health')


@bp.get('/')
def main():
	exercise_list = [
		'push_up.png', 'squat.png', 'crunch.png',
		'lying_reg_raise.png', 'dips.png', 'bicycle_crunch.png',
		'cross_lunge.png', 'pull_up.png', 'side_lateral_raise.png'
	]
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
	for i in exercise_list:
		print(i)
		print(i[0])
		print(i[0][0])
	print(exercise_list)
	exercise_name = ['푸쉬업', '스쿼트', '크런치']
	return render_template('exercise_page.html', exercise_list=exercise_list)

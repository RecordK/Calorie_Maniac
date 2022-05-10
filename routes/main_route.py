from flask import Blueprint, Flask, render_template, request, session
from graphbase import GraphBase
from datetime import datetime

from python_files.exercise.exercise_history_service import ExerciseHistoryService
from python_files.food.food_info_service import FoodInfoService
from python_files.food.food_history_service import FoodHistoryService

# 버스와 관련된 기능 제공 클래스
# 블루프린트 객체 생성 : 라우트 등록 객체
bp = Blueprint('main', __name__, url_prefix='/main')


@bp.post('/')
def main():
    session['gender'] = request.form['gender-options']  # male, female
    session['age'] = request.form['age']
    session['height'] = request.form['height']
    session['weight'] = request.form['weight']

    return render_template('index.html')


@bp.get('/')
def main_return():
    return render_template('index.html')


@bp.get('/report/daily')
def daily_report():
    # Food
    food_info_service = FoodInfoService()
    food_history_service = FoodHistoryService()
    today = datetime.today().strftime("%Y-%m-%d %H:%M")
    food_today = food_history_service.retrieve_by_today()
    food_info_index = [food.food_index for food in food_today]
    food_info_list = food_info_service.retrieve_by_index(food_info_index)
    nutrition_info = []
    if not food_today:      # 빈 배열 감지
        food_today = '오늘 먹은 음식이 없어요!'
    else:
        for food in food_info_list:
            nutrition_info.append([food.food_carbohydrate, food.food_protein, food.food_fat, food.food_sugars])
    # Exercise
    exercise_history_service = ExerciseHistoryService()
    exercise_today = exercise_history_service.retrieve_by_today()
    exercise_index = [exercise.exercise_list for exercise in exercise_today]
    print(exercise_index)
    exercise_list = exercise_history_service.retrieve_by_index(exercise_index)
    exercise_info = []

    if not exercise_today:
        exercise_today = '몰루'
    else:
        for exercise in exercise_list:
            exercise_info.append(
                [exercise.exercise_list, exercise.exercise_index, exercise.exercise_name, exercise.start_time, exercise.end_time, exercise.exercised_time, exercise.count, exercise.use_kcal, exercise.coin])
    print('======')
    print(exercise_today[0].exercise_name)
    print(exercise_info)
    return render_template('loader/daily_page.html', today=today, food_list=food_today, food_nutrition=nutrition_info,
                           exercise_list=exercise_today, exercise_info=exercise_info, zip=zip)


@bp.get('/report/weekly')
def weekly_report():
    monthly_now = datetime.today().month
    print(monthly_now)

    return render_template('loader/weekly_page.html', month=monthly_now)


@bp.get('/report/monthly')
def monthly_report():
    monthly_now = datetime.today().month
    return render_template('loader/monthly_page.html', month=monthly_now)


@bp.route("/dailyChart/<foodindex>")
def get_pie_chart(foodindex):
    food_info_service = FoodInfoService()
    graph_base = GraphBase()
    v1 = food_info_service.retrieve_by_index(foodindex)
    nut = [v1.food_carbohydrate, v1.food_protein, v1.food_fat, v1.food_sugars]
    kcal = [nut[0] * 4, nut[1] * 4, nut[2] * 9, nut[3] * 4]
    c = graph_base.pie_base(value=kcal)
    return c.dump_options_with_quotes()


@bp.route("/weekChart1")
def get_pie_week_diff_chart1():
    a = gb()
    # value= db에서 꺼내온 먹은 음식 칼로리 값
    # name= 주차
    value = [3000, 5000, 4210, 7466]
    name = ['1주차', '2주차', '3주차', '4주차']
    title = '주차간 비교'
    c = a.pie_base(name, value, title)
    return c.dump_options_with_quotes()


@bp.route("/weekChart2")
def get_pie_week_diff_chart2():
    # a = gb()
    # value= db에서 꺼내온 운동한 칼로리  값
    # name= 주차
    # value = [2000, 500, 1421, 746]
    # name = ['1주차', '2주차', '3주차', '4주차']
    # title = '주차간 비교'
    # c = a.pie_base(name, value, title)
    # return c.dump_options_with_quotes()
    pass


@bp.route("/lineGraph")
def get_line_month_graph():
    a = gb()
    c = a.line_month_base()
    return c.dump_options_with_quotes()

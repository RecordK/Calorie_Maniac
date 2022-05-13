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
    session['user'] = session['gender'] + session['age'] + session['height'] + session['weight']
    # print(session['user'])
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
    if not food_today:  # 빈 배열 감지
        food_today = '오늘 먹은 음식이 없어요!'
    else:
        for food in food_info_list:
            nutrition_info.append([food.food_carbohydrate, food.food_protein, food.food_fat, food.food_sugars])
    # Exercise
    exercise_history_service = ExerciseHistoryService()
    # print(exercise_history_service)
    exercise_today = exercise_history_service.retrieve_by_today()
    # print('exercise_today:', exercise_today)
    exercise_index = [exercise.exercise_list for exercise in exercise_today]
    exercise_list = exercise_history_service.retrieve_by_index(exercise_index)
    exercise_info = []

    if not exercise_today:
        exercise_today = '.'
    else:
        for exercise in exercise_today:
            exercise_info.append(
                [exercise.exercise_list, exercise.exercise_index, exercise.exercise_name, exercise.start_time,
                 exercise.end_time, exercise.exercised_time, exercise.count, exercise.use_kcal, exercise.coin,
                 exercise.month, exercise.week, exercise.day, exercise.image])
    return render_template('loader/daily_page.html', today=today, food_list=food_today, food_nutrition=nutrition_info,
                           exercise_list=exercise_today, exercise_info=exercise_info, zip=zip)


@bp.get('/report/weekly')
def weekly_report():
    monthly_now = datetime.today().month
    # print(monthly_now)

    return render_template('loader/weekly_page.html', month=monthly_now)


@bp.get('/report/monthly')
def monthly_report():
    monthly_now = datetime.today().month
    return render_template('loader/monthly_page.html', month=monthly_now)


@bp.route("/dailyChart/<foodindex>/<i>")
def get_pie_chart(foodindex, i):
    food_info_service = FoodInfoService()
    graph_base = GraphBase()
    v1 = food_info_service.retrieve_by_index(foodindex)
    nut = [v1.food_carbohydrate, v1.food_protein, v1.food_fat, v1.food_sugars]
    kcal = [nut[0] * 4, nut[1] * 4, nut[2] * 9, nut[3] * 4]
    c = graph_base.pie_base(value=kcal)
    return c.dump_options_with_quotes()


def ffff():
    food_info_service = FoodInfoService()
    monthly_now = datetime.today().month
    # print(monthly_now)
    # Test Code
    food_history_service = FoodHistoryService()

    # Month Logic
    monthly_now = datetime.today().month
    food_month = food_history_service.retrieve_by_month(monthly_now)
    food_index = [food.food_index for food in food_month]
    food_month_list = food_history_service.retrieve_by_index(food_index)
    food_month_info = []

    if not food_month:
        food_month = '.'
    else:
        for food in food_month_list:
            food_month_info.append(
                [food.food_index, food.food_name, food.food_kcal, food.food_date, food.food_month, food.food_week])

    # Week Logic
    #     print('week_1: ', exercise_month_info[3][10])
    # while True:
    name = set()
    h = set()
    value = []

    fw = dict()
    for i in range(0, len(food_month_info)):
        h.add(food_month_info[i][5])
        for lll in range(1, 6):
            if food_month_info[i][5] == lll:
                name.add('{}주차'.format(lll))

                fw[lll] = 0

                food_week_list = food_history_service.retrieve_by_week(lll)
                food_week_info = []

                if not food_week_list:
                    food_week_list = '.'
                else:
                    for food in food_week_list:
                        food_week_info.append(
                            [food.food_index, food.food_name, food.food_kcal, food.food_kcal, food.food_month,
                             food.food_week])

                    ## 00주차에 해당되는 리스트 다 불러옴
                    for j in range(0, len(food_week_info)):
                        fw[lll] = fw[lll] + int(food_week_info[j][2])
    value = list(dict(sorted(fw.items(), key=lambda x: x[0])).values())
    for i in range(6):
        try:
            value.remove(0)
        except:
            continue
    title = '주차간 비교'
    name = sorted(name)
    return name, value, title, fw


@bp.route("/weekChart1")
def get_pie_week_diff_chart1():
    graph_base = GraphBase()
    name, value, title, fw = ffff()
    c = graph_base.pie_base(name, value, title)
    return c.dump_options_with_quotes()


def exer():
    monthly_now = datetime.today().month
    # print(monthly_now)
    # Test Code
    exercise_history_service = ExerciseHistoryService()

    # Month Logic
    monthly_now = datetime.today().month
    exercise_month_list = exercise_history_service.retrieve_by_month(monthly_now)
    exercise_month_info = []

    if not exercise_month_list:
        exercise_month_list = '.'
    else:
        for exercise in exercise_month_list:
            exercise_month_info.append(
                [exercise.exercise_list, exercise.exercise_index, exercise.exercise_name, exercise.start_time,
                 exercise.end_time, exercise.exercised_time, exercise.count, exercise.use_kcal, exercise.coin,
                 exercise.month, exercise.week])

    # Week Logic
    #     print('week_1: ', exercise_month_info[3][10])
    # while True:
    name = set()
    h = set()
    value = []

    ew = dict()
    for i in range(0, len(exercise_month_info)):
        h.add(exercise_month_info[i][10])
        for lll in range(1, 6):
            if exercise_month_info[i][10] == lll:
                name.add('{}주차'.format(lll))

                ew[lll] = 0

                exercise_week_list = exercise_history_service.retrieve_by_week(lll)
                exercise_week_info = []

                if not exercise_week_list:
                    exercise_week_list = '.'
                else:
                    for exercise in exercise_week_list:
                        exercise_week_info.append(
                            [exercise.exercise_list, exercise.exercise_index, exercise.exercise_name,
                             exercise.start_time,
                             exercise.end_time, exercise.exercised_time, exercise.count, exercise.use_kcal,
                             exercise.coin,
                             exercise.month, exercise.week])

                    ## 00주차에 해당되는 리스트 다 불러옴
                    for j in range(0, len(exercise_week_info)):
                        ew[lll] = ew[lll] + int(exercise_week_info[j][7])

    value = list(dict(sorted(ew.items(), key=lambda x: x[0])).values())
    for i in range(6):
        try:
            value.remove(0)
        except:
            continue
    title = '주차간 비교'
    name = sorted(name)
    return name, value, title, ew


@bp.route("/weekChart2")
def get_pie_week_diff_chart2():
    graph_base = GraphBase()
    name, value, title, ew = exer()
    c = graph_base.pie_base(name, value, title)
    return c.dump_options_with_quotes()


@bp.route("/weekChart3")
def get_pie_week_diff_chart3():
    graph_base = GraphBase()
    a = exer()
    b = ffff()
    ew = a[3]
    fw = b[3]
    ext = dict()

    print(ew, fw)
    f = set(fw.keys())
    e = set(ew.keys())
    ## 있는 것만
    # for i in (f - e):
    #     ew[i] = 0
    # for i in (e - f):
    #     fw[i] = 0
    # for i in (f or b):
    #     ext[i] = fw[i] - ew[i]
    h = {i for i in range(1, 6)}
    ## 없는 것도 포함
    for i in (h - e):
        ew[i] = 0
    for i in (h - f):
        fw[i] = 0
    for i in h:
        ext[i] = fw[i] - ew[i]

    # h = f or b
    h = sorted(h)
    value = list(dict(sorted(ext.items(), key=lambda x: x[0])).values())
    title = '주차간 비교'
    name = []
    h = list(h)
    for i in h:
        name.append('{}주차'.format(i))
    name = sorted(name)
    c = graph_base.bar_base(h, value, title)
    return c.dump_options_with_quotes()


@bp.route("/lineGraph")
def get_line_month_graph():
    month = request.form.get('select_month')
    print('month:', month)
    graph_base = GraphBase()
    monthly_now = datetime.today().month
    # print(monthly_now)

    # Test Code
    exercise_history_service = ExerciseHistoryService()

    # Month Logi
    monthly_now = datetime.today().month
    exercise_month_list = exercise_history_service.retrieve_by_month(monthly_now)
    exercise_month_info = []

    if not exercise_month_list:
        exercise_month_list = '몰루'
    else:
        for exercise in exercise_month_list:
            exercise_month_info.append(
                [exercise.use_kcal, exercise.month,
                 exercise.day])

    execercise_days = dict()
    m = int(str(datetime.today().month))
    end = int(str(datetime.today().day))
    d = []
    if monthly_now < m:
        d = [l for l in range(1, 32)]
    else:
        d = [l for l in range(1, end + 1)]
    for e in d:
        execercise_days[e] = 0

    for i in range(0, len(exercise_month_info)):
        for j in d:
            if exercise_month_info[i][2] == j:
                execercise_days[j] = execercise_days[j] + exercise_month_info[i][0]

                # print('=========', execercise_days[j], exercise_month_info[i][0])

    # print(execercise_days)
    # # 데이터 삽입
    day_exercise_total_kcal = list(execercise_days.values())
    # print(day_exercise_total_kcal)

    ## Food Section
    # Test Code
    food_history_service = FoodHistoryService()

    # Month Logic
    monthly_now = datetime.today().month
    food_month_list = food_history_service.retrieve_by_month(monthly_now)
    food_month_info = []

    if not food_month_list:
        food_month_list = '.'
    else:
        for food in food_month_list:
            food_month_info.append(
                [food.food_index, food.food_name, food.food_kcal, food.food_month,
                 food.food_day])

    days = dict()
    m = int(str(datetime.today().month))
    end = int(str(datetime.today().day))
    d = []
    if monthly_now < m:
        d = [l for l in range(1, 32)]
    else:
        d = [l for l in range(1, end + 1)]
    for l in d:
        days[l] = 0

    for i in range(0, len(food_month_info)):
        for j in d:
            if food_month_info[i][4] == j:
                days[j] = days[j] + food_month_info[i][2]

                # print('=========', days[j], food_month_info[i][2])

    # print(days)

    # # 데이터 삽입
    day_food_total_kcal = list(days.values())
    # print(day_food_total_kcal)
    c = graph_base.line_month_base(d, day_exercise_total_kcal, day_food_total_kcal)
    return c.dump_options_with_quotes()

from flask import Blueprint, Flask, render_template, request, session
from graphbase import GraphBase as gb
from datetime import datetime

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
    today = datetime.today().strftime("%Y-%m-%d %H:%M")
    print(today)  # sql 조회 문으로 바꿔야 함!!!
    food_list = ['food_list', '밥', '공기', '자갈치']
    return render_template('loader/daily_page.html', today=today, food_list=food_list)


@bp.get('/report/weekly')
def weekly_report():
    monthly_now = datetime.today().month
    print(monthly_now)

    return render_template('loader/weekly_page.html', month=monthly_now)


@bp.get('/report/monthly')
def monthly_report():
    monthly_now = datetime.today().month
    return render_template('loader/monthly_page.html', month=monthly_now)


@bp.route("/dailyChart")
def get_pie_chart():
    a = gb()
    c = a.pie_base()
    return c.dump_options_with_quotes()


@bp.route("/weekChart1")
def get_pie_week_diff_chart1():
    a = gb()
    # value= db에서 꺼내온 먹은 음식 칼로리 값
    # key= 주차
    value = [3000, 5000, 4210, 7466]
    key = ['1주차', '2주차', '3주차', '4주차']
    title = '주차간 비교'
    c = a.pie_base(value, key, title)
    return c.dump_options_with_quotes()


@bp.route("/weekChart2")
def get_pie_week_diff_chart2():
    a = gb()
    # value= db에서 꺼내온 운동한 칼로리  값
    # key= 주차
    value = [2000, 500, 1421, 746]
    key = ['1주차', '2주차', '3주차', '4주차']
    title = '주차간 비교'
    c = a.pie_base(value, key, title)
    return c.dump_options_with_quotes()


@bp.route("/lineGraph")
def get_line_month_graph():
    a = gb()
    c = a.line_month_base()
    return c.dump_options_with_quotes()

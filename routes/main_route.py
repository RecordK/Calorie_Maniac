from flask import Blueprint, Flask, render_template, request, session
from graphbase import GraphBase as gb
import os

# 버스와 관련된 기능 제공 클래스

# 블루프린트 객체 생성 : 라우트 등록 객체
bp = Blueprint('main', __name__, url_prefix='/main')


@bp.post('/')
def main():
    session['gender'] = request.form['gender-options']      # male, female
    session['age'] = request.form['age']
    session['height'] = request.form['height']
    session['weight'] = request.form['weight']

    return render_template('index.html')

@bp.get('/')
def main_return():
    return render_template('index.html')


@bp.route("/pieChart")
def get_pie_chart():
    a = gb()
    c = a.pie_base()
    return c.dump_options_with_quotes()


@bp.route("/pie2Chart")
def get_pie_week_diff_chart():
    a = gb()
    c = a.pie_base()
    return c.dump_options_with_quotes()


@bp.route("/lineGraph")
def get_line_month_graph():
    a = gb()
    c = a.line_month_base()
    return c.dump_options_with_quotes()
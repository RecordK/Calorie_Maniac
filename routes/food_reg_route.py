from flask import Blueprint, Flask, render_template, request, session

# 버스와 관련된 기능 제공 클래스

# 블루프린트 객체 생성 : 라우트 등록 객체
bp = Blueprint('food', __name__, url_prefix='/food')

@bp.route('/')
def food():
    return render_template('food.html')
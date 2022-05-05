from flask import Blueprint, Flask, render_template, request, session
from datetime import datetime

bp = Blueprint('health', __name__, url_prefix='/main/health')


@bp.get('/')
def main():
	
	return render_template('exercise_page.html')


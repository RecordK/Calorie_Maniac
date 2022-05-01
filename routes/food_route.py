from flask import Blueprint, Flask, render_template, request, session
from python_files.food.food_info_service import FoodInfoService

bp = Blueprint('food', __name__, url_prefix='/main/food')
food_info_service = FoodInfoService()


@bp.get('/')
def food_page():
	food_list = food_info_service.retrieve_all()
	return render_template('food_page.html', food_list=food_list)


@bp.post('/search')
def food_search():
	food_name = request.form['food_name']
	print(food_name)
	food_list = food_info_service.retrieve_name(food_name)
	print(type(food_list))
	return render_template('loader/food_list.html', food_list=food_list)

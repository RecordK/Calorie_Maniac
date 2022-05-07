from _datetime import datetime
from flask import Blueprint, Flask, render_template, request, session
from python_files.food.food_info_service import FoodInfoService
from python_files.food.food_history_service import FoodHistoryService

bp = Blueprint('food', __name__, url_prefix='/main/food')
food_info_service = FoodInfoService()
food_history_service = FoodHistoryService()

@bp.get('/')
def food_page():
	return render_template('food_page.html')


@bp.post('/search')
def food_search():
	food_name = request.form['food_name']
	food_name = '%' + food_name + '%'
	food_list = food_info_service.retrieve_by_name(food_name)
	return render_template('loader/food_list.html', food_list=food_list)


@bp.get('/register')
def get_index():
	food_info_index = request.args.get('fid')
	food = food_info_service.retrieve_by_index(food_info_index)
	food_image = None
	food_history_service.insert_data(food.food_index, food.food_name, food_image)
	return render_template('index.html')


@bp.post('/upload_food')
def get_food_img():
	food_image = request.files['food_image']
	print(food_image)
	return "done"

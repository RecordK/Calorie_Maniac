from flask import Blueprint, render_template, request
import os
from python_files.food import food_info
from python_files.food.food_info_service import FoodInfoService

bp = Blueprint('root', __name__, url_prefix='/root')
food_info_service = FoodInfoService()


@bp.get('/')
def root():
	pk_key = os.urandom(12).hex()
	print(pk_key)
	return render_template('root_page.html', pk_key=pk_key, confirm=None)


@bp.post('/each_food')
def register_food():
	food = food_info.FoodInfo(
		0, request.form['food_name'], request.form['kcal'], request.form['carbohydrate'],
		request.form['protein'], request.form['fat'], request.form['sugars']
	)
	confirm = food_info_service.insert_food(food)
	return render_template('root_page.html', confirm=confirm)


@bp.post('/file_food')
def register_foods():
	food_file = request.files['food_file']
	file_type = food_file.filename.split('.')[1]
	confirm = food_info_service.insert_foods(food_file, file_type)
	return render_template('root_page.html', confirm=confirm)

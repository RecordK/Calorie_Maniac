from _datetime import datetime
from flask import Blueprint, Flask, render_template, request, session
from python_files.food.food_info_service import FoodInfoService
from python_files.food.food_history_service import FoodHistoryService
from yolov3 import detect_1231 as d
from werkzeug.utils import secure_filename
import os
import cv2

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
    food = 0
    base_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    path = os.path.join(base_path, 'yolov3/data/samples')
    food_image = request.files['food_image']

    food_image.save(path + '/' + secure_filename(food_image.filename))
    food_image_file = cv2.imread(path +'/' + secure_filename(food_image.filename), cv2.IMREAD_UNCHANGED)
    an = d.detect()
    an = check(an)

    food_index = an[0]
    if isinstance(food_index, int):
        food = food_info_service.retrieve_by_index(food_index)
    i = os.listdir(path)
    for j in i:
        os.remove(path + '/' + j)
    return render_template('food_page.html', an=an, food=food, food_image=food_image_file)


def check(x):
    for i in x:
        if len(x) > 1 and type(i) == str:
            x.remove('사진을 다시 등록해주세요')
    if len(set(x)) != len(x):
        x = set(x)

    return x

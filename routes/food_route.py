import os
from datetime import datetime

from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename
from yolov3 import detect_1231 as d

from python_files.food.food_history_service import FoodHistoryService
from python_files.food.food_info_service import FoodInfoService

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
    food_image = 'images/food/' + food_info_index + '.jpg'       # 이미지 없을때 기본 경로
    fd_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    food_time = datetime.strptime(fd_time, "%Y-%m-%d %H:%M:%S")
    # print('data type: ' , type(food_time))
    # print('date : ' , food_time)
    food_date = datetime.today().strftime("%Y-%m-%d")
    y = int(food_date.split('-')[0])
    m = int(food_date.split('-')[1])
    d = int(food_date.split('-')[2])
    food_week = food_history_service.get_week_no(y, m, d)
    food_month = datetime.today().strftime("%m")
    food_day = datetime.today().strftime("%d")
    food_history_service.insert_data(food.food_index, food.food_name, food.food_kcal, fd_time, food_image, food_month, food_week, food_day)
    return render_template('index.html')


@bp.post('/register')
def upload_food_with_image():
    food_index = request.form['food_index']
    food_path = request.form['food_path']
    print(food_index, food_path)
    food = food_info_service.retrieve_by_index(food_index)

    food_date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    year = datetime.today().year
    month = datetime.today().month
    day = datetime.today().day
    food_week = food_history_service.get_week_no(year, month, day)
    food_month = datetime.today().strftime("%m")
    food_day = datetime.today().strftime("%d")
    food_history_service.insert_data(food.food_index, food.food_name, food.food_kcal, food_date, food_path, food_month, food_week,food_day)
    return render_template('index.html')


@bp.post('/wrong')
def delete_img():
    food_path = request.form['food_path']
    food_path = 'static/' + food_path
    base_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    path = os.path.join(base_path, food_path)
    if os.path.exists(path):
        os.remove(path)
    return render_template('food_page.html')


@bp.post('/upload_food')
def get_food_img():
    food_image = request.files['food_image']
    food = 0

    base_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    path = os.path.join(base_path, 'yolov3/data/samples')
    img_path = os.path.join(base_path, 'static/save_img')

    file_today = datetime.today().strftime("%Y%m%d%H%M%S_")
    food_image.save(path + '/' + file_today + secure_filename(food_image.filename))

    an = d.detect()
    an = check(an)

    food_index = an[0]
    if isinstance(food_index, int):
        food = food_info_service.retrieve_by_index(food_index)
    i = os.listdir(path)
    for j in i:
        os.replace(path + '/' + j, img_path + '/' + j)
    food_image_file_path = img_path + '/' + file_today + secure_filename(food_image.filename)
    path_list = food_image_file_path.split('/')
    image_path = path_list[-2] + '/' + path_list[-1]
    print(image_path)
    return render_template('food_page.html', an=an, food=food, image_path=image_path)


def check(x):
    for i in x:
        if len(x) > 1 and type(i) == str:
            x.remove('사진을 다시 등록해주세요')
    if len(set(x)) != len(x):
        x = set(x)

    return x

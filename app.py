import os
from datetime import timedelta

from flask import Flask, render_template

from routes.exercise_route import bp as exercise_bp
from routes.food_route import bp as food_bp
from routes.main_route import bp as main_bp
from routes.root_route import bp as root_bp

app = Flask(__name__, static_folder="./static")
app.config['SECRET_KEY'] = os.urandom(12).hex()
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
app.register_blueprint(main_bp)
app.register_blueprint(root_bp)
app.register_blueprint(food_bp)
app.register_blueprint(exercise_bp)


@app.route('/')
def hello_world():  # put application's code here
    return render_template("start_page.html")


if __name__ == "__main__":
    app.run(debug=True)

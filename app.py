from flask import Flask, render_template
from routes.main_route import bp as main_bp
from routes.root_route import bp as root_bp
import os

app = Flask(__name__, static_folder="./static")
app.config['SECRET_KEY'] = os.urandom(12).hex()
app.register_blueprint(main_bp)
app.register_blueprint(root_bp)


@app.route('/')
def hello_world():  # put application's code here
    return render_template("start_page.html")


if __name__ == "__main__":
    app.run()

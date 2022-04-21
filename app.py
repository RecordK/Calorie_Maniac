from flask import Flask, render_template
from routes.main_route import bp as main_bp


app = Flask(__name__, static_folder="./static")
app.register_blueprint(main_bp)


@app.route('/')
def hello_world():  # put application's code here
    return render_template("start_page.html")


if __name__ == "__main__":
    app.run()

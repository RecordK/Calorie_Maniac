from flask import Flask, render_template
from routes.food_reg_route import bp as food_reg_bp
from graphbase import GraphBase as gb

app = Flask(__name__, static_folder="./static")
app.register_blueprint(food_reg_bp)


@app.route('/')
def hello_world():  # put application's code here
    return render_template("start_page.html")

@app.route("/main")
def index():
    return render_template("index.html")


@app.route("/pieChart")
def get_pie_chart():
    a = gb()
    c = a.pie_base()
    return c.dump_options_with_quotes()


@app.route("/pie2Chart")
def get_pie_week_diff_chart():
    a = gb()
    c = a.pie_week_diff_base()
    return c.dump_options_with_quotes()


@app.route("/lineGraph")
def get_line_month_graph():
    a = gb()
    c = a.line_month_base()
    return c.dump_options_with_quotes()


if __name__ == "__main__":
    app.run()

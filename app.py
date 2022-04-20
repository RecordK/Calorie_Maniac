
from flask import Flask, render_template, request, blueprints
from routes.food_reg_route import bp as food_reg_bp
from random import randrange

from flask import Flask, render_template
from pyecharts.globals import ThemeType
from pyecharts import options as opts
from pyecharts.charts import Bar,Pie


app = Flask(__name__, static_folder="templates")


def pie_base() -> Pie:
    a = [123,456,789,999]
    v = [[i] for i in a]
    k = ['탄수화물','당류','단백질','지방']
    d=[[j] for j in k]
    c = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS)
            ).add("", [list(z) for z in zip(k, v)],rosetype="radius", radius=["30%", "60%"]
                                                                   ).set_series_opts(label_opts=opts.LabelOpts(is_show=True, position='top')
                                                                                     ).set_global_opts(title_opts=opts.TitleOpts(title="음식 영양 정보"),
                     legend_opts=opts.LegendOpts(type_='scroll', pos_bottom="60%", pos_right="-3%", orient="vertical",legend_icon='pin'))
    )
    return c


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/pieChart")
def get_pie_chart():
    c = pie_base()
    return c.dump_options_with_quotes()


if __name__ == "__main__":
    app.run()
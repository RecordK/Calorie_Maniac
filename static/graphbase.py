from pyecharts.globals import ThemeType
from pyecharts import options as opts
from pyecharts.charts import Line, Pie

class GraphBase:
    def pie_base(self) -> Pie:
        a = [123, 456, 789, 999]
        v = [[i] for i in a]
        k = ['탄수화물', '당류', '단백질', '지방']
        c = (
            Pie(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS)
                ).add("", [list(z) for z in zip(k, v)], rosetype="radius", radius=["30%", "60%"]
                      ).set_series_opts(label_opts=opts.LabelOpts(is_show=True, position='top')
                                        ).set_global_opts(title_opts=opts.TitleOpts(title="음식 영양 정보"),
                                                          legend_opts=opts.LegendOpts(type_='scroll', pos_bottom="60%",
                                                                                      pos_right="-3%",
                                                                                      orient="vertical",
                                                                                      legend_icon='pin'))
        )
        return c

    def line_month_base(self) -> Line:
        l = ()
        return l
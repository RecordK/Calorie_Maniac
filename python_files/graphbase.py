from pyecharts.globals import ThemeType
from pyecharts import options as opts
from pyecharts.charts import Line, Pie
from random import randrange


class GraphBase:
    def pie_base(self, values) -> Pie:
        # a = value
        # v = [[i] for i in a]
        # k = name
        # p = (
        #     Pie(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS)
        #         ).add("", [list(z) for z in zip(k, v)], rosetype="radius", radius=["30%", "60%"]
        #               ).set_series_opts(label_opts=opts.LabelOpts(is_show=True, position='top', formatter="{d} %")
        #                                 ).set_global_opts(title_opts=opts.TitleOpts(title=title),
        #                                                   tooltip_opts=opts.TooltipOpts(formatter="{b}: {c} kcal"),
        #                                                   legend_opts=opts.LegendOpts(type_='scroll', pos_bottom="60%",
        #                                                                               pos_right="0%",
        #                                                                               orient="vertical",
        #                                                                               legend_icon='pin'))
        # )
        # return p
        title = '음식 영양 정보'
        name = ['탄수화물', '단백질', '지방', '당류']
        value = [[i] for i in values]
        print(value)
        pie_graph = (Pie(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS)
                 ).add("", [list(z) for z in zip(name, values)], rosetype="radius", radius=["30%", "60%"]
                       ).set_series_opts(
                            label_opts=opts.LabelOpts(
                                is_show=True, position='top', formatter="{d} %")
                                 ).set_global_opts(
                                        title_opts=opts.TitleOpts(title=title),
                                        tooltip_opts=opts.TooltipOpts(formatter="{b}: {c} kcal"),
                                        legend_opts=opts.LegendOpts(
                                            type_='scroll',
                                            pos_bottom="60%",
                                            pos_right="0%",
                                            orient="vertical",
                                            legend_icon='pin'
                                        )
                                )
        )

        return pie_graph


    def line_month_base(self) -> Line:
        ## 꺾은 선 그래프
        day = [i for i in range(1, 21)]
        ex = [randrange(1000, 3000) for _ in range(20)]
        ex2 = [randrange(1000, 3000) for _ in range(20)]
        total_job_rate = Line(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS
                                                      , animation_opts=opts.AnimationOpts(animation_delay=1000
                                                                                          ,
                                                                                          animation_easing="elasticOut")))
        total_job_rate.add_xaxis(day).add_xaxis(day).add_yaxis('운동한 칼로리', ex)

        ## 추가 꺾은선
        l = (Line(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS,
                                          animation_opts=opts.AnimationOpts(animation_delay=1000,
                                                                            animation_easing="elasticOut")
                                          ))).set_global_opts(
            title_opts=opts.TitleOpts(
                title="월간 리포트", subtitle="월간 리포트를 활용하여 효과적으로 칼로리를 계산해보세요!"),
            yaxis_opts=opts.AxisOpts(name="kcal", name_location="top", type_="value"),
            xaxis_opts=opts.AxisOpts(name='날짜', axislabel_opts=opts.LabelOpts(rotate=0)),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
            legend_opts=opts.LegendOpts(pos_left="40%", legend_icon='pin'),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross")
        ).set_series_opts(label_opts=opts.LabelOpts(is_show=True)).add_xaxis(day
                                                                             ).add_yaxis('먹은 음식 칼로리', ex2)

        ## 합치기
        l = l.overlap(total_job_rate)

        return l

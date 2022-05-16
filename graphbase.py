from pyecharts import options as opts
from pyecharts.charts import Line, Pie, Bar
from pyecharts.globals import ThemeType
import numpy as np


class GraphBase:
    def pie_base(self, name=['탄수화물', '단백질', '지방', '당류'], value=[123, 456, 789, 321], title='음식 영양 정보') -> Pie:
        a = value
        v = [[i] for i in a]
        k = name
        p = (
            Pie(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS)
                ).add("", [list(z) for z in zip(k, v)], rosetype="radius", radius=["30%", "60%"]
                      ).set_series_opts(label_opts=opts.LabelOpts(is_show=True, position='top', formatter="{d} %")
                                        ).set_global_opts(title_opts=opts.TitleOpts(title=title),
                                                          tooltip_opts=opts.TooltipOpts(formatter="{b}: {c} kcal"),
                                                          legend_opts=opts.LegendOpts(type_='scroll', pos_bottom="60%",
                                                                                      pos_right="0%",
                                                                                      orient="vertical",
                                                                                      legend_icon='pin'))
        )
        return p

    def bar_base(self, name, value, title) -> Bar:
        # 연도별 취업현황
        attr = name
        b = (Bar(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS,
                                         animation_opts=opts.AnimationOpts(
                                             animation_delay=1000, animation_easing="elasticOut"
                                         ))).add_xaxis(attr
                                                       ).set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            yaxis_opts=opts.AxisOpts(min_='Datamin', name="kcal", type_="value"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=0)),
            legend_opts=opts.LegendOpts(pos_right="10%", pos_top="5%", legend_icon='pin'),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross")
        ).set_series_opts(
            label_opts=opts.LabelOpts(is_show=False))).overlap(Bar(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS)
                                                                   ).add_xaxis(attr)
                                                               .add_yaxis('kcal', value))

        return b

    def test(self, name, value, title) -> Line:
        base = Line(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS
                                            , animation_opts=opts.AnimationOpts(animation_delay=1000
                                                                                ,
                                                                                animation_easing="elasticOut")))
        base.add_xaxis(name).add_yaxis('운동한 칼로리', value)

        ## 추가 꺾은선
        l = (Line(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS,
                                          animation_opts=opts.AnimationOpts(animation_delay=1000,
                                                                            animation_easing="elasticOut")
                                          ))).set_global_opts(
            title_opts=opts.TitleOpts(
                title=title),
            yaxis_opts=opts.AxisOpts(name="kcal", type_="value"),
            xaxis_opts=opts.AxisOpts(name='주차', type_="value"),
            # datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="slider")],
            # legend_opts=opts.LegendOpts(pos_left="40%", legend_icon='pin'),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross")
        ).set_series_opts(label_opts=opts.LabelOpts(is_show=True)).add_xaxis(name
                                                                             )

        ## 합치기
        l = l.overlap(base)

        return l

    def line_month_base(self, day, exercise_kcal, food_kcal) -> Line:
        base = Line(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS,
                                            animation_opts=opts.AnimationOpts(animation_delay=1000,
                                                                              animation_easing="elasticOut")
                                            )
                    )
        base.add_xaxis(day).add_yaxis('운동한 칼로리', np.round(exercise_kcal, 2))

        # 추가 꺾은선
        l = (Line(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS,
                                          animation_opts=opts.AnimationOpts(animation_delay=1000,
                                                                            animation_easing="elasticOut")
                                          ))).set_global_opts(
            title_opts=opts.TitleOpts(title="월간 리포트"),
            yaxis_opts=opts.AxisOpts(name="kcal", type_="value"),
            xaxis_opts=opts.AxisOpts(name='날짜', type_="value"),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="slider")],
            legend_opts=opts.LegendOpts(pos_left="40%", legend_icon='pin'),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross")
        ).set_series_opts(
            label_opts=opts.LabelOpts(is_show=True)
        ).add_xaxis(day).add_yaxis('먹은 음식 칼로리', np.round(food_kcal, 2))


        # 합치기
        l = l.overlap(base)

        return l

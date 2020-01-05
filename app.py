from flask import Flask,redirect,render_template, request
import numpy as np
import csv, os
from pyecharts.charts import Bar, Tab, Line, Map, Timeline, Grid, Scatter
from pyecharts import options as opts
import pandas as pd
from pyecharts.faker import Faker

from pyecharts.charts import Map
from pyecharts import options as opts
from pyecharts.globals import ChartType, SymbolType
import plotly as py
import plotly.graph_objs as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Flask(__name__)
dash_app = dash.Dash(__name__, external_stylesheets=external_stylesheets,server=app,url_base_pathname='/dash/')

df = pd.read_csv("/home/lsm/mysite/data/min_AFR.csv", encoding='GBK', index_col='CountryName')
Netherlands = list(df.loc['Netherlands'].values)[-4:]
Finland = list(df.loc['Finland'].values)[-4:]
Korea = list(df.loc['Korea'].values)[-4:]
Luxembourg = list(df.loc['Luxembourg'].values)[-4:]
dfa = pd.read_csv('/home/lsm/mysite/data/Adolescent_fertility_rate.csv', encoding='utf8')
dfa1 = dfa.dropna(axis=0, how='any')
regions_available = list(dfa.CountryName.dropna().unique())


dash_df = pd.read_csv('/home/lsm/mysite/data/FinalData.csv')
available_indicators = dash_df['Indicator Name'].unique()
dash_app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Fertility rate, total (births per woman)'
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Life expectancy at birth, total (years)'
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
        id='year--slider',
        min=dash_df['Year'].min(),
        max=dash_df['Year'].max(),
        value=dash_df['Year'].max(),
        marks={str(year): str(year) for year in dash_df['Year'].unique()},
        step=None
    )
])

# @app.route('/dash',methods=['GET'])
# def dash():
#     return redirect('/pathname')


@dash_app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value'),
     Input('xaxis-type', 'value'),
     Input('yaxis-type', 'value'),
     Input('year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = dash_df[dash_df['Year'] == year_value]

    return {
        'data': [dict(
            x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': dict(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

@app.route('/', methods=['GET'])
def index():
    dfa = pd.read_csv('/home/lsm/mysite/data/data.csv', encoding='gbk')
    data_str = dfa.to_html()
    return render_template('index.html',the_res=data_str,the_select_region=regions_available)

@app.route('/story', methods=['GET'])
def story():
    return render_template('story.html')

@app.route('/new', methods=['GET'])
def new():
    return app.send_static_file('new.html')


@app.route('/search',methods=['POST'])
def search():
    dfa = pd.read_csv('/home/lsm/mysite/data/data.csv', encoding='gbk')
    area = request.form.to_dict()['area']
    areaData = dfa.query("CountryName=='{}'".format(area)).sort_values(by="Year" , ascending=True).to_dict('records')
    year = []
    gdp = []
    rate = []
    for i in areaData:
        year.append(i['Year'])
        if i['IndicatorName'] == 'GDP':
            gdp.append(i['Value'])
        else:
            rate.append(i['Value'])
    year = list(set(year))
    year.sort()
    bar = Bar()
    bar.add_xaxis(year)
    bar.add_yaxis(area,rate)
    bar.add_yaxis(area,gdp)
    bar.set_global_opts(title_opts=opts.TitleOpts(title=area+"青少年生育率/国民生产总值GDP"))
    bar.render('/home/lsm/mysite/templates/search.html')
    return render_template('search.html')

@app.route('/afr', methods=['GET'])
def arf():
    dfa = pd.read_csv('/home/lsm/mysite/data/Adolescent_fertility_rate.csv', encoding='utf8')
    dfa1 = dfa.dropna(axis=0, how='any')

    def timeline_map() -> Timeline:
        tl = Timeline()
        for i in range(2010, 2017):
            map0 = (
                Map()
                    .add(
                    "青少年怀孕率", (list(zip(list(dfa1.CountryName), list(dfa1["{}".format(i)])))), "world",
                    is_map_symbol_show=False
                )
                    .set_global_opts(
                    title_opts=opts.TitleOpts(title="".format(i), subtitle="",
                                              subtitle_textstyle_opts=opts.TextStyleOpts(color="red", font_size=16,
                                                                                         font_style="italic")),
                    visualmap_opts=opts.VisualMapOpts(min_=0, max_=100, series_index=0),

                )
            )
            tl.add(map0, "{}".format(i))
        return tl
    timeline_map().render('/home/lsm/mysite/templates/afr.html')
    return render_template('afr.html')

@app.route('/gdp', methods=['GET'])
def gdp():
    dfb = pd.read_csv('/home/lsm/mysite/data/GDP.csv', encoding='utf8')
    dfb1 = dfb.dropna(axis=0, how='any')
    def timeline_map() -> Timeline:
        tl = Timeline()
        for i in range(2010, 2017):
            map0 = (
                Map()
                    .add(
                    "全球人均GDP", (list(zip(list(dfb1.CountryName), list(dfb1["{}".format(i)])))), "world",
                    is_map_symbol_show=False
                )
                    .set_global_opts(
                    title_opts=opts.TitleOpts(title="".format(i), subtitle="",
                                              subtitle_textstyle_opts=opts.TextStyleOpts(color="red", font_size=16,
                                                                                         font_style="italic")),
                    visualmap_opts=opts.VisualMapOpts(min_=0, max_=100, series_index=0),

                )
            )
            tl.add(map0, "{}".format(i))
        return tl
    timeline_map().render('/home/lsm/mysite/templates/gdp.html')
    return render_template('gdp.html')

@app.route('/gdp_afp', methods=['GET'])
def gdp_afp():
    df = pd.read_csv("/home/lsm/mysite/data/GDPandAFP_max.csv", encoding='GBK')
    def grid_vertical() -> Grid:
        bar = (
            Bar()
                .add_xaxis(list(df.country))
                .add_yaxis("青少年怀孕率最高八国GDP", list(df.GDP))
                .set_global_opts(title_opts=opts.TitleOpts(title="青少年怀孕率最高八国GDP"))
        )
        line = (
            Line()
                .add_xaxis(list(df.country))
                .add_yaxis("青少年怀孕率最高八国青少年怀孕率", list(df.Adolescent_fertility_rate))
                .set_global_opts(
                title_opts=opts.TitleOpts(title="青少年怀孕率最高八国青少年怀孕率", pos_top="48%"),
                legend_opts=opts.LegendOpts(pos_top="48%"),
            )
        )

        grid = (
            Grid()
                .add(bar, grid_opts=opts.GridOpts(pos_bottom="60%"))
                .add(line, grid_opts=opts.GridOpts(pos_top="60%"))
        )
        return grid
    grid_vertical().render('/home/lsm/mysite/templates/gdp_afp.html')
    return render_template('gdp_afp.html')

@app.route('/min_afr', methods=['GET'])
def min_afr():
    dfe = pd.read_csv("/home/lsm/mysite/data/education.csv", index_col=0)
    dfe.head()
    dfe.columns = [int(x) for x in dfe.columns]
    dfe.index = ['Finland', 'Mali']
    dfe.head()
    dfe.loc["Finland", :]
    Finland = go.Scatter(
        x=[pd.to_datetime('01/01/{y}'.format(y=x), format="%m/%d/%Y") for x in dfe.columns.values],
        y=dfe.loc["Finland", :].values,
        name="Finland"
    )

    Mali = go.Scatter(
        x=[pd.to_datetime('01/01/{y}'.format(y=x), format="%m/%d/%Y") for x in dfe.columns.values],
        y=dfe.loc["Mali", :].values,
        name="Mali"
    )

    layout = dict(xaxis=dict(rangeselector=dict(buttons=list([
        dict(count=1,
             label="1年",
             step="year",
             stepmode="backward"),
        dict(count=2,
             label="2年",
             step="year",
             stepmode="backward"),
        dict(count=3,
             label="3年",
             step="year",
             stepmode="backward"),
        dict(count=4,
             label="4年",
             step="year",
             stepmode="backward"),
        dict(step="all")
    ])),
        rangeslider=dict(bgcolor="#70EC57"),
        title='年份'
    ),
        yaxis=dict(title='两国教育程度对比图'),
        title="两国教育程度对比图"
    )

    fig = dict(data=[Finland, Mali], layout=layout)
    py.offline.plot(fig, filename="/home/lsm/mysite/templates/min_afr.html",auto_open=False)
    return render_template('min_afr.html')

@app.route('/max_afr', methods=['GET'])
def max_afr():
    df = pd.read_csv("/home/lsm/mysite/data/max_AFR.csv", encoding='GBK', index_col='CountryName')
    Angola = list(df.loc['Angola'].values)[-4:]
    Mali = list(df.loc['Mali'].values)[-4:]
    Chad = list(df.loc['Chad'].values)[-4:]
    Niger = list(df.loc['Niger'].values)[-4:]
    BurkinaFaso = list(df.loc['BurkinaFaso'].values)[-4:]
    CentralAfricaRepublic = list(df.loc['CentralAfricaRepublic'].values)[-4:]
    EquatorialGuinea = list(df.loc['EquatorialGuinea'].values)[-4:]
    Zambia = list(df.loc['Zambia'].values)[-4:]

    def timeline_map() -> Timeline:
        tl = Timeline()
        for i in range(2010, 2017):
            map0 = (
                Map()
                    .add(
                    "青少年怀孕率", (list(zip(list(dfa1.CountryName), list(dfa1["{}".format(i)])))), "world",
                    is_map_symbol_show=False
                )
                    .set_global_opts(
                    title_opts=opts.TitleOpts(title="".format(i), subtitle="",
                                              subtitle_textstyle_opts=opts.TextStyleOpts(color="red", font_size=16,
                                                                                         font_style="italic")),
                    visualmap_opts=opts.VisualMapOpts(min_=0, max_=100, series_index=0),

                )
            )
            tl.add(map0, "{}".format(i))
        return tl

    def overlap_line_scatter() -> Bar:
        x = list(['2014', '2015', '2016', '2017'])
        bar = (
            Bar()
                .add_xaxis(x)
                .add_yaxis("Netherlands", Netherlands)
                .add_yaxis("Finland", Finland)
                .add_yaxis("Korea", Korea)
                .add_yaxis("Luxembourg", Luxembourg)
                .set_global_opts(title_opts=opts.TitleOpts(title="青少年怀孕率最低四国数据"))
        )
        line = (
            Line()
                .add_xaxis(x)
                .add_yaxis("Netherlands", Netherlands)
                .add_yaxis("Finland", Finland)
                .add_yaxis("Korea", Korea)
                .add_yaxis("Luxembourg", Luxembourg)
        )
        bar.overlap(line)
        return bar

    def data() -> Bar:
        x = list(['2014', '2015', '2016', '2017'])
        bar = (
            Bar()
                .add_xaxis(x)
                .add_yaxis("Angola", Angola)
                .add_yaxis("Mali", Mali)
                .add_yaxis("Chad", Chad)
                .add_yaxis("Niger", Niger)
                .add_yaxis("BurkinaFaso", BurkinaFaso)
                .add_yaxis("CentralAfricaRepublic", CentralAfricaRepublic)
                .add_yaxis("EquatorialGuinea", EquatorialGuinea)
                .add_yaxis("Zambia", Zambia)

                .set_global_opts(title_opts=opts.TitleOpts(title="Top8"))
        )

        return bar

    tab = Tab()
    tab.add(timeline_map(), "2010~2017青少年怀孕率地图")
    tab.add(data(), "2014~2017青少年怀孕率最高八个国家数据")
    tab.add(overlap_line_scatter(), "最低四国数据图")
    tab.render('/home/lsm/mysite/templates/max_afr.html')
    return render_template('max_afr.html')


if __name__ == '__main__':
    app.run(debug=True, port=8000)

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import Flask, render_template, url_for
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/estherc1/NOSO/master/Jialan_Zhu/AR_data_flask/usjh_AR_itemlist_flask.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='US Jewerly House Dashboard - Basket Analysis by Line Item'),


    html.Label('Choose your item(s)'),
    dcc.Dropdown(
        id='dropdown-a',
        options=[{'label': i, 'value': i} for i in df['lineitem_name'].unique()],
        value='',
        multi=True
    ),
    html.Div(id='input-a'),

    html.Label('Choose your sale item(s)'),
        dcc.Dropdown(
        id='dropdown-b',
        options=[{'label': i, 'value': i} for i in df['lineitem_name'].unique()],
        value='',
        multi=True
    ),
    html.Div(id='input-b')
])

@app.callback(
    dash.dependencies.Output('input-a', 'children'),
    [dash.dependencies.Input('dropdown-a', 'value')])
def callback_a(dropdown_value):
    return 'You\'ve selected the following item(s): "{}"'.format(dropdown_value)

@app.callback(
    dash.dependencies.Output('input-b', 'children'),
    [dash.dependencies.Input('dropdown-b', 'value')])
def callback_a(dropdown_value):
    return 'You\'ve selected the following item(s): "{}"'.format(dropdown_value)


if __name__ == '__main__':
    app.run_server(debug=True)

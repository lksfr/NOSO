# -*- coding: utf-8 -*-
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import pandas as pd
import flask
import plotly.plotly as py
from plotly import graph_objs as go
import math

df = pd.read_csv(
    'https://gist.githubusercontent.com/lksfr/c65d53e66ef45673ce4c8f5ef23e2645/raw/c3dc295facb571959dccc917797158b81d032ac2/CLV.csv',
    index_col=False)

df = df.drop("Unnamed: 0", axis=1)

app = dash.Dash()

app.layout = html.Div([
        # header
        html.Div([
            html.Div(
                html.Img(src='https://i.ibb.co/G74pSt4/transparant.png',height="100%")
                ,style={"float":"left","height":"100%", "margin-top": "0px"})
            ],
            className="row header",style={"background-color": "#ffffff"}
            ),

        # tabs
        html.Div([
            dcc.Tabs(id="tabs", children=[
                html.Div([
                dcc.Tab(label='Clustering', 
                        style={"height":"20","verticalAlign":"middle", "text-align": "center"},
                        children=[
                        #styling
                        html.Link(href="https://use.fontawesome.com/releases/v5.2.0/css/all.css",rel="stylesheet"),
                        html.Link(href="https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",rel="stylesheet"),
                        html.Link(href="https://fonts.googleapis.com/css?family=Dosis", rel="stylesheet"),
                        html.Link(href="https://fonts.googleapis.com/css?family=Open+Sans", rel="stylesheet"),
                        html.Link(href="https://fonts.googleapis.com/css?family=Ubuntu", rel="stylesheet"),
                        html.Link(href="https://cdn.rawgit.com/amadoukane96/8a8cfdac5d2cecad866952c52a70a50e/raw/cd5a9bf0b30856f4fc7e3812162c74bfc0ebe011/dash_crm.css", rel="stylesheet"),

                        html.H3("Customer Lifetime Value", style={"padding-left": "150px"}),

                        dcc.Dropdown(id='dropdown', style={'width': '60%', "padding-left": "150px"}, options=[
                            {'label': i, 'value': i} for i in df.ID.unique()
                            ], multi=True, placeholder='Filter by customer address...'),

                        html.Div(
                            html.H3("Customer Return Probability")
                            ,style={"float":"right","height":"100%", "padding-right": "150px", "margin-top": "-105px"}),

                        html.Br(),

                        dcc.Dropdown(id='dropdown2', style={'width': '60%', "padding-left": "150px"}, options=[
                            {'label': i, 'value': i} for i in df.Target_Group.unique()
                            ], multi=True, placeholder='Filter by target group...'),

                        html.Div([

                            dt.DataTable(
                            # Initialise the rows
                            rows=df.to_dict("records"),
                            row_selectable=True,
                            filterable=True,
                            sortable=True,
                            selected_row_indices=[],
                            id='table'
                        )                            
                        ], style = {'width':'800px'})
                    ])
                ]),

                dcc.Tab(label='CLV', 
                        style={"height":"20","verticalAlign":"middle", "text-align": "center"},
                        children=[
                    html.Div([
                        html.Link(href="https://use.fontawesome.com/releases/v5.2.0/css/all.css",rel="stylesheet"),
                        html.Link(href="https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",rel="stylesheet"),
                        html.Link(href="https://fonts.googleapis.com/css?family=Dosis", rel="stylesheet"),
                        html.Link(href="https://fonts.googleapis.com/css?family=Open+Sans", rel="stylesheet"),
                        html.Link(href="https://fonts.googleapis.com/css?family=Ubuntu", rel="stylesheet"),
                        html.Link(href="https://cdn.rawgit.com/amadoukane96/8a8cfdac5d2cecad866952c52a70a50e/raw/cd5a9bf0b30856f4fc7e3812162c74bfc0ebe011/dash_crm.css", rel="stylesheet"),

                        html.H3("Some CLV Analysis")
                    ])
                ]),

                dcc.Tab(label='Cases', 
                        style={"height":"20","verticalAlign":"middle", "text-align": "center"},
                        children=[
                    html.Div([
                        html.Link(href="https://use.fontawesome.com/releases/v5.2.0/css/all.css",rel="stylesheet"),
                        html.Link(href="https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",rel="stylesheet"),
                        html.Link(href="https://fonts.googleapis.com/css?family=Dosis", rel="stylesheet"),
                        html.Link(href="https://fonts.googleapis.com/css?family=Open+Sans", rel="stylesheet"),
                        html.Link(href="https://fonts.googleapis.com/css?family=Ubuntu", rel="stylesheet"),
                        html.Link(href="https://cdn.rawgit.com/amadoukane96/8a8cfdac5d2cecad866952c52a70a50e/raw/cd5a9bf0b30856f4fc7e3812162c74bfc0ebe011/dash_crm.css", rel="stylesheet"),

                        html.H3("Placeholder")
                    ])
                ])
            ])
        ])
    ])
                 

@app.callback(
    dash.dependencies.Output('table', 'rows'),
    [Input('dropdown', 'value'), Input('dropdown2', 'value')])

def update_table(dropdown, dropdown2):
    if dropdown is None and dropdown2 is None:
        return df.to_dict("records")

    else:
        dff = df[(df["Target_Group"].str.contains('|'.join(dropdown2))) & (df["ID"].str.contains('|'.join(dropdown)))]
        return dff.to_dict("records")


if __name__ == "__main__":
    app.run_server(debug=True)
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

# return html Table with dataframe values  
def generate_table(dataframe, max_rows=50):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


#returns most significant part of a number
def millify(n):
    n = float(n)
    millidx = max(
        0,
        min(
            len(millnames) - 1, int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))
        ),
    )

    return "{:.0f}{}".format(n / 10 ** (3 * millidx), millnames[millidx])


#returns top indicator div
def indicator(color, text, id_value):
    return html.Div(
        [
            
            html.P(
                text,
                className="twelve columns indicator_text"
            ),
            html.P(
                id = id_value,
                className="indicator_value"
            ),
        ],
        className="four columns indicator",
        
    )

app = dash.Dash()


app.layout = html.Div(
    [
        # header
        html.Div([


          # html.Div(
           # html.Span("USJH Dashboard", className='app-title', style={"color": "black", "padding-bottom": "-40px"}),
           # ),
            html.Div(
                html.Img(src='https://i.ibb.co/G74pSt4/transparant.png',height="100%")
                ,style={"float":"left","height":"100%", "margin-top": "0px"})
            ],
            className="row header",style={"background-color": "#ffffff"}
            ),

        # tabs
        html.Div([

            dcc.Tabs(
                id="tabs",
                style={"height":"20","verticalAlign":"middle", "text-align": "center"},
                children=[
                    dcc.Tab(label="Clustering", value="opportunities_tab"),
                    dcc.Tab(label="CLV", value="leads_tab"),
                    dcc.Tab(id="...",label="Cases", value="cases_tab"),
                ],
                value="leads_tab",
            )

            ],
            className="row tabs_div"
            ),
       
                
        # divs that save dataframe for each tab
       
       


        # Tab content
        html.Div(id="tab_content", className="row", style={"margin": "2% 3%"}),
        
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


        html.Div(id='table-container', style={'width': '36%', "padding-left": "150px"})
            ],
            className="row",
            style={"margin": "0%"}
)

@app.callback(
    dash.dependencies.Output('table-container', 'children'),
    [Input('dropdown', 'value'), Input('dropdown2', 'value')])
def display_table(dropdown, dropdown2):
    if dropdown is None and dropdown2 is None:
        return generate_table(df)

    dff = df[(df["Target_Group"].str.contains('|'.join(dropdown2))) & (df["ID"].str.contains('|'.join(dropdown)))]
    return generate_table(dff)





@app.callback(Output("tab_content", "children"), [Input("tabs", "value")])
def render_content(tab):
    if tab == "opportunities_tab":
        return opportunities.layout
    elif tab == "cases_tab":
        return cases.layout
    elif tab == "leads_tab":
        return leads.layout
    else:
        return opportunities.layout

if __name__ == "__main__":
    app.run_server(debug=True)
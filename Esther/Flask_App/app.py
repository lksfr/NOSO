import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import Flask, render_template, url_for
import pandas as pd
from sfManager import sf_Manager

usjh_AR = pd.read_csv(
    'https://gist.githubusercontent.com/JialanZ/7143ed3673ab585a23552d4916e2fd45/raw/fd1e5797e4938fc5bc5b4ce3d5edd048a21a598f/usjh_item_flask.csv',
    index_col=False)
rules_ = pd.read_csv(
    'https://gist.githubusercontent.com/JialanZ/7143ed3673ab585a23552d4916e2fd45/raw/fd1e5797e4938fc5bc5b4ce3d5edd048a21a598f/rule_support_flask.csv',
    index_col=False)
rulec_ = pd.read_csv(
    'https://gist.githubusercontent.com/JialanZ/7143ed3673ab585a23552d4916e2fd45/raw/fd1e5797e4938fc5bc5b4ce3d5edd048a21a598f/rule_confidence_flask.csv',
    index_col=False)




external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='US Jewerly House Dashboard - Basket Analysis by Line Item'),


    html.Label('Item(s) on Sale!'),
    dcc.Dropdown(
        id='dropdown1',
        options=[{'label': i, 'value': i} for i in usjh_AR['lineitem_name'].unique()],
        value='',
        multi=True
    ),
    html.Div(id='input1'),

    html.Label('Choose your item(s)'),
        dcc.Dropdown(
        id='dropdown2',
        options=[{'label': i, 'value': i} for i in usjh_AR['lineitem_name'].unique()],
        value='',
        multi=True
    ),
    html.Div(id='input2'),


    html.H3("Customer Lifetime Value", style={"padding-left": "150px"}),
    html.Div(id='input3')
])

@app.callback(
    dash.dependencies.Output('input1', 'children'),
    [dash.dependencies.Input('dropdown1', 'value')])
def callback_a(dropdown_value):
    return 'You\'ve selected the following item(s): "{}"'.format(dropdown_value)

@app.callback(
    dash.dependencies.Output('input2', 'children'),
    [dash.dependencies.Input('dropdown2', 'value')])
def callback_a(dropdown_value):
    return 'You\'ve selected the following sale item(s): "{}"'.format(dropdown_value)

@app.callback(
    dash.dependencies.Output('input3', 'children'),
    [dash.dependencies.Input('dropdown1', 'value'),dash.dependencies.Input('dropdown2', 'value')])
def prodcut_recommendation(dropdown1, dropdown2, usjh_AR, rules_, rulec_):
    sale=set(dropdown1)
    order=set(dropdown2)

    #create the data frame for sale
    s={'lineitem_name':[], 'vendor_category':[], 'frequency':[]}
    for item in sale:
        s['lineitem_name'].append(item)
        s['vendor_category'].append(usjh_AR[usjh_AR['lineitem_name']==item].vendor_category.iloc[0])
        s['frequency'].append(usjh_AR[usjh_AR['lineitem_name']==item].frequency.iloc[0])
    
    sale=pd.DataFrame(s)
    #
    #creat (vendor:category) basing on sale and order
    sale_vc=[]
    for item in sale['lineitem_name']:
        sale_vc.append(usjh_AR[usjh_AR['lineitem_name']==item].vendor_category.iloc[0])
    
    sale_vc=set(sale_vc)
    #
    order_vc=[]
    for item in order:
        order_vc.append(usjh_AR[usjh_AR['lineitem_name']==item].vendor_category.iloc[0])
    
    order_vc=set(order_vc)
    #
    #recommendation basing on the highest support 
    #lookup the association rules
    assoc_rules={'rhs':[], 'support':[]}

    for item in order_vc:
        if len(rules_[rules_['lhs']==item].rhs)>0: #some items have no rules_
            assoc_rules['rhs'].append(rules_[rules_['lhs']==item].rhs.iloc[0])
            assoc_rules['support'].append(rules_[rules_['lhs']==item].support.iloc[0])

    assoc_rules=pd.DataFrame(assoc_rules)

    rhs=assoc_rules.sort_values('support', ascending=False)

    #check if there is on sale item
    recommend=''
    r_support=0
    for item in rhs['rhs']:
    #if there are items on sale in rhs, return the one with the greatest support
        if item in sale_vc:
            if rhs[rhs['rhs']==item].support.iloc[0] > r_support:
                recommend=item
                r_support=rhs[rhs['rhs']==item].support.iloc[0]

    #make recommendations basing on recommend
    #if recommend is not empty, which means this is associated on item on sale, recommand the top 3
    if recommend != '':
        rec_items=sale[sale['vendor_category']==recommend].sort_values('frequency',ascending=False)
        #if len(rec_items['lineitem_name'].unique())>3:
        #rec_items=rec_items['lineitem_name'].unique()[:3]
         #else:
        rec_items=rec_items['lineitem_name'].unique()
    #if there is no on sale item, the recommend will be an empty string, 
    #then just simply choose the item with the highest support in rhs
    else :
        recommend=rhs['rhs'].iloc[0]
#now we have the final recommend, pick the specific items to make recommendation
#find the lineitem name in recommend with top 3 frequency
    
    rec_items=usjh_AR[usjh_AR['vendor_category']==recommend].sort_values('frequency',ascending=False).lineitem_name
#there are a lot of duplicated items, get the unique top 3
    rec_items=rec_items.unique()[:3]

    return rec_items


if __name__ == '__main__':
    app.run_server(debug=True)
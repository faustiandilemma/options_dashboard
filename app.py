import pandas as pd
import numpy as np
import datetime as dt
import requests
import os

import plotly.graph_objects as go
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
#import dash_bootstrap_components as dbc
#from plotly.subplots import make_subplots


#app stuff
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
server.secret_key = os.environ.get('SECRET_KEY', 'default-value-used-in-development')
app.title=tabtitle

#app layout
app.layout = html.Div([
    html.Div([
        html.H4('Price Feed'),
        html.Div(id='live-update-price'),
        html.I('Select an expiry'),
        dcc.Interval(
            id='time interval',
            interval=5*1000, # in milliseconds
            n_intervals=0
        )
    ]),
])
@app.callback(Output('live-update-price', 'children'),
              [Input('time interval', 'n_intervals')])

def price_update(n):
    resp1 = requests.get('https://deribit.com/api/v2/public/get_index?currency=BTC', params={
    "jsonrpc": "2.0",
    "method": "public/get_index",
    "id": 42,
    "params": {
        "currency": "BTC"}
})
    dbit_btc=resp1.json()
    btc_price=dbit_btc['result']['BTC']
    return html.Div([dcc.Markdown('''btc price is {:.2f}'''.format(btc_price))])


if __name__ == '__main__':
    app.run_server()

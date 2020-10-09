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

#saved price data
bstamp_old = pd.read_csv('bitstamp_historical.csv')

#app stuff
#external_stylesheets = [dbc.themes.DARKLY]
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
server.secret_key = os.environ.get('SECRET_KEY', 'default-value-used-in-development')

#app layout
app.layout = html.Div([
html.H3('Options Dashboard'),
#tab1
dcc.Tabs([
    dcc.Tab(label='Max Pain', children=[
        html.Div([
        html.Label('Select an expiry'),
        dcc.RadioItems(
            id='options expiry tab1',
            options=[,
                {'label': 'Oct 16th, 2020', 'value': 'SYN.BTC-16OCT20'},
                {'label': 'Oct 23rd, 2020', 'value': 'SYN.BTC-23OCT20'},
                {'label': 'Oct 30th, 2020', 'value': 'SYN.BTC-30OCT20'},
                {'label': 'Dec 25th, 2020', 'value': 'BTC-25DEC20'},
                {'label': 'March 26th, 2021', 'value': 'BTC-26MAR21'},
                {'label': 'June 25th, 2021', 'value': 'BTC-25JUN21'}
        ],
            value = 'SYN.BTC-16OCT20',
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Graph(
            id = 'max pain graph',
            ),
        ]),
        html.B('Feedback or issues? '),
        html.A('Contact here',href="https://twitter.com/FaustianDilemma"),
        html.Br(),
        html.B('Tutorial and discussion '),
        html.A('here',href="https://discord.gg/2yqtVXa")
]),
#tab2
    dcc.Tab(label='Historical Vol Data', children=[
        html.Label('Select realized volatility duration'),
        dcc.Dropdown(
            id='vol dropdown 1',
            options=[
                {'label': '10 day realized volatility', 'value': '10 day realized vol'},
                {'label': '30 day realized volatility', 'value': '30 day realized vol'},
                {'label': '90 day realized volatility', 'value': '90 day realized vol'}
        ],
            value='10 day realized vol'
    ),
        dcc.Graph(
            id='vol distribution graph',
    ),
        dcc.Checklist(
            id = 'vol checklist',
            options=[
                {'label': '10 day realized volatility', 'value': '10 day realized vol'},
                {'label': '30 day realized volatility', 'value': '30 day realized vol'},
                {'label': '90 day realized volatility', 'value': '90 day realized vol'}
        ],
            value=['10 day realized vol'],
            labelStyle={'display': 'inline-block'}
),
        dcc.Graph(
            id = 'realized vol graph',
            )
]),
    
#tab3
    dcc.Tab(label='Historical Forecast', children=[
        html.Label('Select realized volatility duration'),
        dcc.Dropdown(
            id='dropdown vol 2',
            options=[
                {'label': '10 day realized volatility', 'value': '10 day realized vol'},
                {'label': '30 day realized volatility', 'value': '30 day realized vol'},
                {'label': '90 day realized volatility', 'value': '90 day realized vol'}
        ],
            value='10 day realized vol'
    ),
        dcc.RadioItems(
            id='inequality buttons',
            options=[
                {'label': '<', 'value': '<'},
                {'label': '>', 'value': '>'}
    ],
        value='<',
        labelStyle={'display': 'inline-block'}
    ), 
        dcc.Slider(
            id='vol slider',
            min=0,
            max=300,
            step=5,
            value=50,
            marks={
                0:'0',
                25:'25',
                50:'50',
                75:'75',
                100:'100',
                150:'150',
                200:'200',
                250:'250',
                300:'300',
        }
    ),
        dcc.Dropdown(
            id='forecast dropdown',
            options=[
                {'label': '5 day forecast', 'value': '5'},
                {'label': '10 day forecast', 'value': '10'},
                {'label': '30 day forecast', 'value': '30'}
        ],
            value='5'
    ),
        dcc.Graph(
            id='vol forecast graph',
    ),
        dcc.Dropdown(
            id='return forecast dropdown',
            options=[
                {'label': '5 day return forecast', 'value': '5'},
                {'label': '10 day return forecast', 'value': '10'},
                {'label': '30 day return forecast', 'value': '30'}
        ],
            value='5'
    ),
        dcc.Graph(
            id='return forecast graph'
    ),
        dash_table.DataTable(
            id = 'decile table',
            columns = [{"id": x, "name": x} for x in ['decile', 'forecast returns decile range (%)']],
            style_table={'overflowX': 'auto'},
            style_cell={
                'height': 'auto',
                # all three widths are needed
                'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                'whiteSpace': 'normal'
            }
        ),
        ]),
#tab 4
    dcc.Tab(label='Options Analysis', children=[
    html.Div([
        html.B('Enter the option and volatility criteria below to see the distribution of future returns and the probability of the option being in the money based on historical data'),
        html.Br(),
        dcc.Input(id="btc price", type="number", placeholder=""),
        html.I("Enter current BTC price (round to nearest dollar)"),
        html.Br(),
        html.Label("Select realized vol duration"),
        dcc.RadioItems(
            id='realized vol buttons tab3',
            options=[
                {'label': '10 day realized vol', 'value': '10 day realized vol'},
                {'label': '30 day realized vol', 'value': '30 day realized vol'},
                {'label': '90 day realized vol', 'value': '90 day realized vol'}
            ],
            value = '10 day realized vol',
            labelStyle={'display': 'inline-block'}
        ),
        dcc.RadioItems(
            id='vol inequality choices tab3',
            options=[
                {'label': 'less than', 'value': '<'},
                {'label': 'greater than', 'value': '>'},
                {'label': 'in a 5 point range from current vol', 'value': '5range'},
                {'label': 'in a 10 point range from current vol', 'value': '10range'}
        ],
            value = '<',
            labelStyle={'display': 'inline-block'}
        ),
        #text box for vol number
        dcc.Input(id="vol input tab3", type="number", placeholder=""), #may need to debounce
        html.I("Enter current realized vol here"),
        #buying/selling
        dcc.RadioItems(
            id='buy/sell buttons',
            options=[
                {'label': 'buy', 'value': 'buy'},
                {'label': 'sell', 'value': 'sell'}
            ],
            value = 'buy',
            labelStyle={'display': 'inline-block'}
        ),
        #call/put/straddle
        dcc.RadioItems(
            id='option type',
            options=[
                {'label': 'call', 'value': 'call'},
                {'label': 'put', 'value': 'put'},
                {'label': 'straddle (same calendar strike only)', 'value': 'straddle'}
            ],
            value = 'call',
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Input(id="strike price", type="number", placeholder=""), #may need to debounce
        html.I("Enter strike price"),
        html.Br(),
        #debit/credit amount
        dcc.Input(id="cost input", type="number", placeholder=""), #may need to debounce
        html.I("Enter cost/credit of trade in USD (round to nearest dollar)"),
        #duration (will give you custom forecast) for [button] (vol or return forecast)
        html.Br(),
        dcc.Input(id="duration input", type="number", placeholder=""), #may need to debounce
        html.I("Enter days to expiry"),
        html.Br(),
        html.Button(id='button',n_clicks=None, children='Submit'),
    
        dcc.Graph(
            id = 'returns distribution tab3'
        ),
        dash_table.DataTable(
            id = 'returns decile table tab3',
            columns = [{"id": x, "name": x} for x in ['decile', 'forecast returns decile range (%)']],
            style_table={'overflowX': 'auto'},
            style_cell={
                'height': 'auto',
                # all three widths are needed
                'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                'whiteSpace': 'normal'
            }
        ),
        html.Br(),
    ]),
    html.Div(id='output'),
        ]),
#tab 5
    dcc.Tab(label='Kelly Criterion', children=[
        html.Div([
        #can make different kelly's part of dropdown
        html.B('If you have your past trade data (including win %, avg win, and avg loss), you can enter those numbers in the fields below to see what the optimal risk is based off of the simple version of the Kelly Criterion or a fraction of it.  You can also calculate with a ruin factor for more conservative risk.'),
        html.Br(),
        dcc.Input(id="win rate", type="number", placeholder=""),        
        html.I('Enter win rate (as a decimal)'),
        html.Br(),
        dcc.Input(id="win amount", type="number", placeholder=""),        
        html.I("Enter average win dollar amount"),
        html.Br(),
        dcc.Input(id="loss amount", type="number", placeholder=""),
        html.I("Enter average loss dollar amount"),
        html.Br(),
        html.Label('Select Kelly fraction'),
        dcc.RadioItems(
            id='kelly fraction',
            options=[
                {'label': '100%', 'value': '1'},
                {'label': '90%', 'value': '.9'},
                {'label': '80%', 'value': '.8'},
                {'label': '70%', 'value': '.7'},
                {'label': '60%', 'value': '.6'},
                {'label': '50%', 'value': '.5'}
                ],
            value = '1',
            labelStyle={'display': 'inline-block'}
            ),
        html.Label('Include ruin factor? (this can be the largest past loss amount or can be a simulated figure based on slippage or other unknowns.  Recommended if selling options.)'),
        dcc.RadioItems(
            id='ruin factor',
            options=[
                {'label': 'yes', 'value': 'yes'},
                {'label': 'no', 'value': 'no'}
            ],
            value = 'no',
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Input(id='ruin probability', type="number", placeholder=""),
        html.I('Enter ruin probability as a decimal'),
        html.Br(),
        dcc.Input(id="ruin amount", type="number", placeholder=""),
        html.I('Enter ruin dollar amount'),
        html.Br(),
        html.Button(id='kelly button',n_clicks=None, children='Submit')
    ]),
    html.Div(
        id='kelly result'
    )        
    ]),
]),
])

#callback for tab 1
@app.callback(dash.dependencies.Output('max pain graph', 'figure'),
     [dash.dependencies.Input('options expiry tab1', 'value')])

def max_pain_expiry(expiry_value):
    #calculating max pain
    #dbit api call
    resp1 = requests.get('https://deribit.com/api/v2/public/get_book_summary_by_currency?currency=BTC&kind=option')
    #resp1.ok
    dbit = resp1.json()
    df_oi = pd.DataFrame(dbit['result'], columns=['volume','underlying_index','open_interest', 'instrument_name'])
    pain = df_oi[df_oi['underlying_index']==expiry_value]
    pain1 = pain[['open_interest','instrument_name']]
    if 'SYN' in expiry_value and len(expiry_value)==14:
        pain1['option_strike'] = pain1['instrument_name'].str[11:-2]
    else:
        pain1['option_strike'] = pain1['instrument_name'].str[12:-2]
    pain1['option_strike'] = pd.to_numeric(pain1['option_strike'])
    pain1['option_type'] = pain1['instrument_name'].str[-1]
    calls = pain1[pain1['option_type']== 'C']
    puts = pain1[pain1['option_type']== 'P']
    intrinsic_df = pd.DataFrame(pain1['option_strike'].unique(), columns=['strike'])
    intrinsic_df = intrinsic_df.sort_values(by=['strike'])
    intrinsic_df['intrinsic'] = 0
    intrinsic_df['call intrinsic'] = 0
    intrinsic_df['put intrinsic'] = 0
    call_int = []
    put_int = []
    for value in intrinsic_df['strike']:
        strike_int = []
        pstrike_int = []
        for valueC in calls['option_strike']:
            if valueC < value:
                strike_int.append((value - valueC) * calls.loc[calls['option_strike'] == valueC, 'open_interest'].iloc[0])
        for valueP in puts['option_strike']:
            if valueP > value:
                pstrike_int.append((valueP - value) * puts.loc[puts['option_strike'] == valueP, 'open_interest'].iloc[0])
        put_int.append(sum(pstrike_int))
        call_int.append(sum(strike_int))
    intrinsic_df['put intrinsic'] = put_int
    intrinsic_df['call intrinsic'] = call_int
    intrinsic_df['intrinsic'] = intrinsic_df['call intrinsic'] + intrinsic_df['put intrinsic']
    #graphs
    trace1=go.Bar(name='call oi', x=calls['option_strike'], y=calls['open_interest'])
    trace2=go.Bar(name='put oi', x=puts['option_strike'], y=puts['open_interest'])
    trace3=go.Scatter(name='max pain',x=intrinsic_df['strike'], y=intrinsic_df['intrinsic'],yaxis='y2')
    traces=[trace1,trace2,trace3]
    figure1={
        'data' : traces,
        'layout':{
            'title': 'Max pain and Deribit options open interest',
                'xaxis': {
                    'title':'Strike Price'
                    },
                'yaxis': {
                    'title':'Open Interest',
                    'rangemode' : 'tozero'
                    },
                'yaxis2': {
                    'title': 'Intrinsic Value at Expiry',
                    'overlaying': 'y',
                    'side': 'right',
                    'rangemode' : 'tozero'
                    },
                'barmode':'group',
                'legend': {
                    'x': '1.1'
            },
                'paper_bgcolor':'rgb(233,233,233)',
                'plot_bgcolor':'rgb(233,233,233)'
        }
    }
    return figure1
#callback for tab 2
@app.callback([
    dash.dependencies.Output('vol distribution graph', 'figure'), 
    dash.dependencies.Output('realized vol graph', 'figure')],
    [dash.dependencies.Input('vol dropdown 1', 'value'), dash.dependencies.Input('vol checklist', 'value')])

def update_graph(dropdown_value, checklist_value):
    ###bitstamp api
    periods = '86400'
    resp = requests.get('https://www.bitstamp.net/api/v2/ohlc/btcusd', params={
    'start': '1572739200', # historic starts 8/18/2011, new data from 11/03/2019 onwards
    'step': periods,
    'limit': '1000'
    })
    #resp.ok

    bdata = resp.json()
    bstamp = pd.DataFrame(bdata['data']['ohlc'], columns=[
    'high','timestamp', 'volume', 'low', 'close', 'open'
    ])
    bstamp['date'] = pd.to_datetime(bstamp['timestamp'], unit='s')

    df_list = ['volume', 'close']
    for column in df_list:
        bstamp[column] = pd.to_numeric(bstamp[column])
    data = bstamp_old.append(bstamp)
    data['date'] = pd.to_datetime(data['timestamp'], unit='s')

    data['returns'] = data['close'].pct_change()
    data['% returns'] = data['returns']*100
    rvol_values = [10,30,90,365]
    for value in rvol_values:
        data['stdev'+str(value)] = data['returns'].rolling(value).std()
        data[str(value)+' day realized vol'] = data['stdev'+str(value)]*(365**0.5)*100
    ###
    trace = [go.Histogram(x=data[dropdown_value], opacity=0.75, name='realized vol distribution')]
    dist_figure = {'data' : trace,
            'layout': {
                'title': dropdown_value + ' distribution',
                'xaxis': {
                    'title':'volatility (%)'
                },
                'yaxis': {
                    'title':'frequency of volatility'
                }
            }}
    graphs=[]
    if '10 day realized vol' in checklist_value:
        scatter1 = go.Scatter(x=data['date'], y=data['10 day realized vol'], opacity=0.75, name='10 day realized vol')
        graphs.append(scatter1)
    if '30 day realized vol' in checklist_value:
        scatter2 = go.Scatter(x=data['date'], y=data['30 day realized vol'], opacity=0.75, name='30 day realized vol')
        graphs.append(scatter2)
    if '90 day realized vol' in checklist_value:
        scatter3 = go.Scatter(x=data['date'], y=data['90 day realized vol'], opacity=0.75, name='90 day realized vol')
        graphs.append(scatter3)
    scat_figure = {'data': graphs,
           'layout': {
                'title': 'Realized Volatility',
                'yaxis': {
                    'title':'volatility (%)'
            }}}
    return dist_figure, scat_figure

#callback for tab 3
@app.callback([
    dash.dependencies.Output('vol forecast graph', 'figure'),
    dash.dependencies.Output('return forecast graph', 'figure'), 
    dash.dependencies.Output('decile table', 'data')],
    [dash.dependencies.Input('vol slider', 'value'), dash.dependencies.Input('dropdown vol 2', 'value'),
    dash.dependencies.Input('inequality buttons', 'value'), dash.dependencies.Input('forecast dropdown', 'value'),
    dash.dependencies.Input('return forecast dropdown', 'value')])

def update_forecast(slider_value, dropdown_value, inequality_value, forecast_value, return_forecast_value):
    ###bitstamp api
    periods = '86400'
    resp = requests.get('https://www.bitstamp.net/api/v2/ohlc/btcusd', params={
    'start': '1572739200', # historic starts 8/18/2011, new data from 11/03/2019 onwards
    'step': periods,
    'limit': '1000'
    })
    #resp.ok

    bdata = resp.json()
    bstamp = pd.DataFrame(bdata['data']['ohlc'], columns=[
    'high','timestamp', 'volume', 'low', 'close', 'open'
    ])
    bstamp['date'] = pd.to_datetime(bstamp['timestamp'], unit='s')

    df_list = ['volume', 'close']
    for column in df_list:
        bstamp[column] = pd.to_numeric(bstamp[column])
    data = bstamp_old.append(bstamp)
    data['date'] = pd.to_datetime(data['timestamp'], unit='s')

    data['returns'] = data['close'].pct_change()
    data['% returns'] = data['returns']*100
    rvol_values = [10,30,90,365]
    for value in rvol_values:
        data['stdev'+str(value)] = data['returns'].rolling(value).std()
        data[str(value)+' day realized vol'] = data['stdev'+str(value)]*(365**0.5)*100
    ###
    data['forecast'] = data[dropdown_value].shift(-int(forecast_value))
    data['return_forecast'] = ((data['close'].shift(-int(return_forecast_value)) - data['close'])/data['close'])*100
    if inequality_value == '<':
        df = data[data[dropdown_value] < slider_value]
    if inequality_value == '>':
        df = data[data[dropdown_value] > slider_value]
    #df of specified vol inequality for realized vol
    df_forecast = df['forecast']
    #df of specified vol inequality for returns
    df_return = df['return_forecast']
    #returns table
    decile = pd.qcut(df_return, 10,precision=2)
    decile_df = pd.DataFrame(['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th'], columns=['decile'])
    decile_df['forecast returns decile range (%)'] = decile.cat.categories
    decile_values = []
    for value in decile_df['forecast returns decile range (%)']:
        decile_values.append(str(value))
    decile_df['forecast returns decile range (%)'] = decile_values
    #graphs
    vol_forecast = go.Histogram(x=df_forecast, opacity=0.75, name='forecast vol distribution')
    return_forecast = go.Histogram(x=df_return, opacity=0.75, name='return forecast graph')
    forecast ={
        'data': [vol_forecast],
            'layout': {
                'title': forecast_value + ' day forecast of historic vol distribution for ' + dropdown_value + inequality_value
                + str(slider_value),
                'xaxis': {
                    'title':'volatility (%)'
                },
                'yaxis': {
                    'title':'frequency of volatility'
                }
            }}
    forecast1 ={
        'data': [return_forecast],
            'layout': {
                'title': 'Historic ' +  return_forecast_value + ' day return forecast distribution for current realized vol ' + 
                inequality_value + str(slider_value),
                'xaxis': {
                    'title':'return (%)' 
                },
                'yaxis': {
                    'title':'frequency of return'
                }
            }}
    return forecast, forecast1, decile_df.to_dict('rows')

#callback for tab 4
@app.callback([
    dash.dependencies.Output('returns distribution tab3', 'figure'), 
    dash.dependencies.Output('returns decile table tab3', 'data'),
    dash.dependencies.Output('output', 'children')],
    [Input("button", "n_clicks")],
    [dash.dependencies.State('realized vol buttons tab3', 'value'), 
    dash.dependencies.State('vol inequality choices tab3', 'value'),
    dash.dependencies.State('vol input tab3', 'value'), dash.dependencies.State('duration input', 'value'),
    dash.dependencies.State('btc price', 'value'), dash.dependencies.State('strike price', 'value'),
    dash.dependencies.State('cost input', 'value'), dash.dependencies.State('buy/sell buttons', 'value'),
    dash.dependencies.State('option type', 'value')])

def expected_return(n_clicks,realized_vol, inequality_value, vol_value, duration_value, btc_price, strike_price,
                    cost, buy_sell, option_type):
    if n_clicks is None:
        return dash.no_update
    else:
        ###bitstamp api
        periods = '86400'
        resp = requests.get('https://www.bitstamp.net/api/v2/ohlc/btcusd', params={
        'start': '1572739200', # historic starts 8/18/2011, new data from 11/03/2019 onwards
        'step': periods,
        'limit': '1000'
        })
        #resp.ok

        bdata = resp.json()
        bstamp = pd.DataFrame(bdata['data']['ohlc'], columns=[
        'high','timestamp', 'volume', 'low', 'close', 'open'
        ])
        bstamp['date'] = pd.to_datetime(bstamp['timestamp'], unit='s')

        df_list = ['volume', 'close']
        for column in df_list:
            bstamp[column] = pd.to_numeric(bstamp[column])
        data = bstamp_old.append(bstamp)
        data['date'] = pd.to_datetime(data['timestamp'], unit='s')

        data['returns'] = data['close'].pct_change()
        data['% returns'] = data['returns']*100
        rvol_values = [10,30,90,365]
        for value in rvol_values:
            data['stdev'+str(value)] = data['returns'].rolling(value).std()
            data[str(value)+' day realized vol'] = data['stdev'+str(value)]*(365**0.5)*100
        ###
        data['forecast returns'] = ((data['close'].shift(-duration_value) - data['close'])/data['close'])*100
        if inequality_value == '<':
            vol_df = data[data[realized_vol] < vol_value]
        if inequality_value == '>':
            vol_df = data[data[realized_vol] > vol_value]
        if inequality_value == '5range':
            vol_df = data[data[realized_vol].between((vol_value-5), (vol_value+5), inclusive=True)]
        if inequality_value == '10range':
            vol_df = data[data[realized_vol].between((vol_value-10), (vol_value+10), inclusive=True)]
        return_forecast = vol_df['forecast returns']
        return_histo = go.Histogram(x=return_forecast, opacity=0.75, name='return forecast graph')
        #graph
        forecast ={
            'data': [return_histo],
                'layout': {
                    'title': 'Historic ' +  str(duration_value) + ' day return forecast distribution for current realized vol ',
                    'xaxis': {
                        'title':'return (%)'
                    },
                    'yaxis': {
                        'title':'frequency of return'
                    }
                }}
        #graph
        forecast ={
            'data': [return_histo],
                'layout': {
                    'title': 'Historic ' +  str(duration_value) + ' day return forecast distribution for current realized vol ',
                    'xaxis': {
                        'title':'return (%)'
                    },
                    'yaxis': {
                        'title':'frequency of return'
                    },
                'paper_bgcolor':'rgb(233,233,233)',
                'plot_bgcolor':'rgb(233,233,233)'
                }}
        #table
        decile = pd.qcut(return_forecast, 10,precision=2)
        decile_df = pd.DataFrame(['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th'], columns=['decile'])
        decile_df['forecast returns decile range (%)'] = decile.cat.categories
        decile_values = []
        for value in decile_df['forecast returns decile range (%)']:
            decile_values.append(str(value))
        decile_df['forecast returns decile range (%)'] = decile_values
        #probability itm for option
        if option_type == 'straddle':
            percent_threshold = (cost/strike_price)*100
        else:    
            percent_threshold = ((abs(btc_price - strike_price)+cost)/btc_price) *100
        straddle_df = abs(return_forecast)
        if buy_sell == 'buy':
            if option_type == 'call':
                prob_itm =(len(return_forecast[return_forecast > percent_threshold])/len(return_forecast))*100
            if option_type == 'put':
                prob_itm =(len(return_forecast[return_forecast < -percent_threshold])/len(return_forecast))*100
            if option_type == 'straddle':
                prob_itm =(len(straddle_df[straddle_df > straddle_threshold])/len(straddle_df))*100
        if buy_sell == 'sell':
            if option_type == 'call':
                prob_itm =(len(return_forecast[return_forecast < percent_threshold])/len(return_forecast))*100
            if option_type == 'put':
                prob_itm =(len(return_forecast[return_forecast > -percent_threshold])/len(return_forecast))*100
            if option_type == 'straddle':
                prob_itm =(len(straddle_df[straddle_df < straddle_threshold])/len(straddle_df))*100
        return forecast, decile_df.to_dict('rows'), html.Div(
            [dcc.Markdown('''**Based on historical returns and the volatility criteria you selected, 
            there is a {:.2f}% of this option being in the money at expiry**'''.format(prob_itm))]
        )
#tab 5 callback
@app.callback(Output('kelly result', 'children'),
               [Input("kelly button", "n_clicks")],
               [State('win rate', 'value'), State('win amount', 'value'), State('loss amount', 'value'), 
               State('ruin factor', 'value'),State('ruin probability','value'), State('ruin amount', 'value'),
               State('kelly fraction', 'value')])

def kelly_output(n_clicks, win_rate, win_amt, loss_amt, ruin_factor, ruin_prob, ruin_amt, k_fraction):
    if n_clicks is None:
        return dash.no_update
    else:
        num=win_rate*(win_amt/loss_amt) - (1-win_rate)*1
        denom=(win_amt/loss_amt)
        bet_size= (num/denom) * float(k_fraction) * 100
        if ruin_factor == 'yes':
            expectation = win_rate*(win_amt/loss_amt) - (1-win_rate)*1 - ruin_prob*(ruin_amt/loss_amt)
            gamma = (win_amt/loss_amt)
            lambda1 = (ruin_amt/loss_amt)
            a = (gamma) * lambda1
            b = -(win_rate*gamma*(1+lambda1) + (1-win_rate)*(gamma-lambda1) + ruin_prob*(lambda1)*((gamma) - 1))
            c = expectation
            root1 = ((-b + np.sqrt(b**2 - 4*a*c))/(2*a))*100
            root2 = ((-b - np.sqrt(b**2 - 4*a*c))/(2*a))*100
            bet_risk = min(root1, root2)*float(k_fraction)
            return html.Div(
            [dcc.Markdown('''**Your maximum trade risk should be {:.2f}% of your bankroll**'''.format(bet_risk))]
        )
        if ruin_factor == 'no':
            return html.Div(
            [dcc.Markdown('''**Your maximum trade risk should be {:.2f}% of your bankroll**'''.format(bet_size))]
        )

if __name__ == '__main__':
    app.run_server()

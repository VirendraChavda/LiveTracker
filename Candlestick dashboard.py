import pip

try:
    from dash import Dash, dcc, html, Input, Output
except:
    pip.main(['install', 'dash'])
    from dash import Dash, dcc, html, Input, Output

try:
    import dash_bootstrap_components as dbc
except:
    pip.main(['install', 'dash_bootstrap_components'])
    import dash_bootstrap_components as dbc

try:
    import plotly.express as px
    import plotly.graph_objects as go
except:
    pip.main(['install', 'plotly.express'])
    import plotly.express as px
    import plotly.graph_objects as go

try:
    import pandas_ta as ta
except:
    pip.main(['install', 'pandas_ta'])
    import pandas_ta as ta

import pandas as pd
import numpy as np
import requests

# Coin options and corresponding display tickers
coin_options = [
    {'label': 'BTC/USD', 'value': 'btcusd'},
    {'label': 'ETH/USD', 'value': 'ethusd'},
    {'label': 'USDT/USD', 'value': 'usdtusd'},
    {'label': 'SOL/USD', 'value': 'solusd'},
    {'label': 'USDC/USD', 'value': 'usdcusd'},
    {'label': 'XRP/USD', 'value': 'xrpusd'},
    {'label': 'DOGE/USD', 'value': 'dogeusd'},
    {'label': 'ADA/USD', 'value': 'adausd'},
    {'label': 'AVAX/USD', 'value': 'avaxusd'},
    {'label': 'SHIB/USD', 'value': 'shibusd'}
]

# Helper function to create dropdowns with adjacent labels and black text for options
def create_dropdown(options, id_value, title, default_value):
    return html.Div([
        html.Label(title, style={'margin-right': '10px', 'display': 'inline-block', 'font-weight': 'bold'}),
        dcc.Dropdown(
            options=options, 
            id=id_value, 
            value=default_value,  # Set the default value
            style={'width': '200px', 'display': 'inline-block', 'color': '#000000'},  # Black text for the options
        )
    ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '10px', 'margin-right': '20px'})

# Create the app layout
app = Dash(external_stylesheets=[dbc.themes.CYBORG])

# App layout
app.layout = html.Div([
    
    html.H2("Crypto Price Tracker", style={'textAlign': 'center', 'color': '#1EC0A9'}),
    html.H6("By Virendrasinh Chavda", style={'textAlign': 'center', 'color': '#C4C4C4', 'margin-bottom': '20px'}),
    
    html.Div([

        # 'Coin Pair' Dropdown
        create_dropdown(coin_options, 'Coin', 'Coin Pair:', 'btcusd'),

        # 'Timeframe' Dropdown
        create_dropdown([{'label': '1 Minute', 'value': '60'}, {'label': '3 Minutes', 'value': '180'}, {'label': '1 Hour', 'value': '3600'}, {'label': '1 Day', 'value': '86400'}], 
                        'Timeframe', 'Timeframe:', '180'),

        # 'Span' Dropdown
        create_dropdown([{'label': '20', 'value': '20'}, {'label': '30', 'value': '30'}, {'label': '50', 'value': '50'}, {'label': '70', 'value': '70'}], 
                        'Span', 'Span:', '30'),  

        # 'Select Indicator' Dropdown aligned with other dropdowns
        html.Div([
            html.Label('Select Indicator:', style={'margin-right': '10px', 'font-weight': 'bold'}),
            dcc.Dropdown(
                id='indicator-dropdown',
                options=[
                    {'label': 'RSI Indicator', 'value': 'RSI'},
                    {'label': 'MACD Indicator', 'value': 'MACD'},
                    {'label': 'Bollinger Bands', 'value': 'Bollinger'},
                    {'label': 'Support and Resistance Levels', 'value': 'SupportResistance'}
                ],
                value='RSI',  # Default value
                style={'width': '200px', 'display': 'inline-block', 'color': '#000000'}
            )
        ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '10px', 'margin-right': '20px'})

    ], style = {'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'margin': 'auto', 'width': '100%'}),
    
    # Wrapped RangeSlider in a Div to apply styling
    html.Div([
        html.Label('Select Range:', style={'margin-right': '10px', 'font-weight': 'bold', 'display': 'inline-block'}),
        html.Div(dcc.RangeSlider(0, 20, 1, value=[0, 20], id='range-slider'), style={'width': '800px', 'display': 'inline-block'})
    ], style = {'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'margin-top': '20px'}),

    dcc.Graph(id="candles"),  # Candlestick chart
    html.H4(""),

    dcc.Graph(id="indicator-chart"),  # Indicator chart placeholder
    html.H4(""),
    dcc.Graph(id="heatmap"),  # Original Heatmap
    
    dcc.Interval(id='interval', interval=10000),

    html.H6("Copyright © Virendrasinh Chavda. All Rights Reserved.", style={'textAlign': 'center', 'color': '#C4C4C4', 'margin-bottom': '20px'}),
])

# Helper functions for technical analysis
def calculate_moving_averages(data):
    data['MA'] = data['close'].astype(float).rolling(window=20).mean()
    data['EMA'] = ta.ema(data['close'].astype(float), length=20)
    return data

def calculate_bollinger_bands(data):
    bb = ta.bbands(data['close'].astype(float), length=20)
    
    # Assign the appropriate columns
    data['BB_lower'] = bb['BBL_20_2.0']
    data['BB_middle'] = bb['BBM_20_2.0']
    data['BB_upper'] = bb['BBU_20_2.0']
    
    return data

def calculate_macd(data):
    macd = ta.macd(data['close'].astype(float))
    data['MACD'] = macd['MACD_12_26_9']
    data['Signal'] = macd['MACDs_12_26_9']
    return data

def calculate_support_resistance(data):
    # Example method to calculate support and resistance
    data['Support'] = data['low'].rolling(window=20).min()
    data['Resistance'] = data['high'].rolling(window=20).max()
    return data

def add_fibonacci_retracement(data):
    # Ensure the data is in numeric format
    data['low'] = data['low'].astype(float)
    data['high'] = data['high'].astype(float)
    
    min_price = data['low'].min()
    max_price = data['high'].max()
    levels = [0.236, 0.382, 0.5, 0.618, 0.786]
    fib_lines = [max_price - (max_price - min_price) * level for level in levels]
    return fib_lines

# Callback to update the charts and heatmap
@app.callback(
    [Output('candles', 'figure'),
     Output('indicator-chart', 'figure'),
     Output('heatmap', 'figure')],
    [Input('interval', 'n_intervals'),
     Input('Coin', 'value'),
     Input('Timeframe', 'value'),
     Input('Span', 'value'),
     Input('range-slider', 'value'),
     Input('indicator-dropdown', 'value')]
)
def update_figure(n_intervals, coin_pair, timeframe, num_bars, range_values, selected_indicator):
    url = f'https://www.bitstamp.net/api/v2/ohlc/{coin_pair}/'
    
    # Fetch OHLC data for the selected coin
    params = {'step': timeframe, 'limit': int(num_bars) + 14}
    data = requests.get(url, params=params).json()['data']['ohlc']
    data = pd.DataFrame(data)
    data.timestamp = pd.to_datetime(data.timestamp, unit='s')
    data['close'] = data['close'].astype(float)
    data['high'] = data['high'].astype(float)
    data['low'] = data['low'].astype(float)

    # Add technical indicators
    data = calculate_moving_averages(data)
    data = calculate_bollinger_bands(data)
    data = calculate_macd(data)
    data = calculate_support_resistance(data)
    data['rsi'] = ta.rsi(data.close.astype(float))
    data = data.iloc[14:]  # remove NaN in RSI
    data = data.iloc[range_values[0]:range_values[1]]

    # Candlestick chart with MA, EMA, Fibonacci as legend toggleable traces
    candles = go.Figure(data=[go.Candlestick(
        x=data.timestamp, open=data.open, high=data.high, low=data.low, close=data.close,
        name="Candlestick"
    )])
    
    # Make other traces hidden by default, using `visible='legendonly'`
    candles.add_trace(go.Scatter(x=data.timestamp, y=data['MA'], mode='lines', name='MA', visible='legendonly'))
    candles.add_trace(go.Scatter(x=data.timestamp, y=data['EMA'], mode='lines', name='EMA', visible='legendonly'))

    # Fibonacci retracement levels as scatter traces for legend toggleability
    fib_lines = add_fibonacci_retracement(data)
    for i, fib in enumerate(fib_lines):
        candles.add_trace(go.Scatter(x=[data.timestamp.min(), data.timestamp.max()],
                                     y=[fib, fib],
                                     mode='lines',
                                     line=dict(dash='dash', color='yellow'),
                                     name=f"Fib Level {i+1}",
                                     visible='legendonly'))

    candles.update_layout(
        title=f"Candlestick Chart",
        title_font=dict(size=20, family='Ariel , sans-serif', color='#C4C4C4', weight='bold'),  
        xaxis_title="Time",
        xaxis_title_font=dict(size=16, family='Ariel , sans-serif', color='#C4C4C4', weight='bold'), 
        xaxis_tickfont=dict(size=14, family='Ariel , sans-serif', color='#C4C4C4', weight='bold'), 
        yaxis_title="Price",
        yaxis_title_font=dict(size=16, family='Ariel , sans-serif', color='#C4C4C4', weight='bold'), 
        yaxis_tickfont=dict(size=14, family='Ariel , sans-serif', color='#C4C4C4', weight='bold'),
        xaxis_rangeslider_visible=False,
        height=500,
        template='plotly_dark',
        transition_duration=500  # Set transition duration to 700
    )

    # Generate the selected indicator chart with transitions
    indicator_chart = go.Figure()

    if selected_indicator == 'RSI':
        indicator_chart.add_trace(go.Scatter(x=data.timestamp, y=data.rsi, mode='lines', name="RSI"))
        indicator_chart.update_layout(
            title="RSI Indicator", 
            xaxis_title="Time", 
            yaxis_title="RSI Value",
            title_font=dict(size=20, family='Ariel , sans-serif', color='#C4C4C4', weight='bold'),
            xaxis_title_font=dict(size=16, family='Ariel , sans-serif', color='#C4C4C4', weight='bold'), 
            xaxis_tickfont=dict(size=14, family='Ariel , sans-serif', color='#C4C4C4', weight='bold'),
            yaxis_title_font=dict(size=16, family='Ariel , sans-serif', color='#C4C4C4', weight='bold'), 
            yaxis_tickfont=dict(size=14, family='Ariel , sans-serif', color='#C4C4C4', weight='bold'),
            template='plotly_dark',
            transition_duration=500  # Ensure transition for RSI
        )
    elif selected_indicator == 'MACD':
        indicator_chart.add_trace(go.Scatter(x=data.timestamp, y=data['MACD'], mode='lines', name='MACD'))
        indicator_chart.add_trace(go.Scatter(x=data.timestamp, y=data['Signal'], mode='lines', name='Signal'))
        indicator_chart.update_layout(
            title="MACD Indicator", 
            xaxis_title="Time", 
            yaxis_title="MACD Value",
            title_font=dict(size=20, family='Ariel , sans-serif', color='#C4C4C4', weight='bold'),
            xaxis_title_font=dict(size=16, family='Ariel , sans-serif', color='#C4C4C4', weight='bold'), 
            xaxis_tickfont=dict(size=14, family='Ariel , sans-serif', color='#C4C4C4', weight='bold'),
            yaxis_title_font=dict(size=16, family='Ariel , sans-serif', color='#C4C4C4', weight='bold'), 
            yaxis_tickfont=dict(size=14, family='Ariel , sans-serif', color='#C4C4C4', weight='bold'),
            template='plotly_dark',
            transition_duration=500  # Ensure transition for MACD
        )
    elif selected_indicator == 'Bollinger':
        indicator_chart.add_trace(go.Scatter(x=data.timestamp, y=data['close'], mode='lines', name='Price'))
        indicator_chart.add_trace(go.Scatter(x=data.timestamp, y=data['BB_upper'], mode='lines', name='BB Upper'))
        indicator_chart.add_trace(go.Scatter(x=data.timestamp, y=data['BB_lower'], mode='lines', name='BB Lower'))
        indicator_chart.update_layout(
            title="Bollinger Bands", 
            xaxis_title="Time", 
            yaxis_title="Price",
            title_font=dict(size=20, family='Ariel , sans-serif', color='#C4C4C4', weight='bold'),
            xaxis_title_font=dict(size=16, family='Ariel , sans-serif', color='#C4C4C4', weight='bold'), 
            xaxis_tickfont=dict(size=14, family='Ariel , sans-serif', color='#C4C4C4', weight='bold'),
            yaxis_title_font=dict(size=16, family='Ariel , sans-serif', color='#C4C4C4', weight='bold'), 
            yaxis_tickfont=dict(size=14, family='Ariel , sans-serif', color='#C4C4C4', weight='bold'), 
            template='plotly_dark',
            transition_duration=500  # Ensure transition for Bollinger Bands
        )
    elif selected_indicator == 'SupportResistance':
        indicator_chart.add_trace(go.Scatter(x=data.timestamp, y=data['Support'], mode='lines', name='Support'))
        indicator_chart.add_trace(go.Scatter(x=data.timestamp, y=data['Resistance'], mode='lines', name='Resistance'))
        indicator_chart.update_layout(
            title="Support and Resistance Levels", 
            xaxis_title="Time", 
            yaxis_title="Price",
            title_font=dict(size=20, family='Ariel , sans-serif', color='#C4C4C4', weight='bold'),
            xaxis_title_font=dict(size=16, family='Ariel , sans-serif', color='#C4C4C4', weight='bold'), 
            xaxis_tickfont=dict(size=14, family='Ariel , sans-serif', color='#C4C4C4', weight='bold'),
            yaxis_title_font=dict(size=16, family='Ariel , sans-serif', color='#C4C4C4', weight='bold'), 
            yaxis_tickfont=dict(size=14, family='Ariel , sans-serif', color='#C4C4C4', weight='bold'), 
            template='plotly_dark',
            transition_duration=500  # Ensure transition for Support/Resistance
        )

    # Heatmap calculation for multiple coins (original)
    coins = [coin['value'] for coin in coin_options]
    tickers = [coin['label'] for coin in coin_options]  # Use tickers for x-axis
    price_changes = []

    for coin in coins:
        coin_url = f'https://www.bitstamp.net/api/v2/ohlc/{coin}/'
        coin_data = requests.get(coin_url, params=params).json()['data']['ohlc']
        df = pd.DataFrame(coin_data)
        df['change'] = df['close'].astype(float).pct_change()  # Calculate percentage change
        price_changes.append(df['change'].iloc[-1])  # Append last change for heatmap

    heatmap_data = pd.DataFrame({'Coins': coins, 'Price Change': price_changes})

    heatmap = go.Figure(
        data=go.Heatmap(
            z=[heatmap_data['Price Change']],
            x=tickers,  # Show tickers on the x-axis
            colorscale='Viridis'
        )
    )
    heatmap.update_layout(
        title="Crypto Price Movement Heatmap",
        xaxis_title="Cryptocurrencies",
        yaxis_title="Price Movement",
        height=300,
        title_font=dict(size=20, family='Ariel , sans-serif', color='#C4C4C4', weight='bold'),
        xaxis_title_font=dict(size=16, family='Ariel , sans-serif', color='#C4C4C4', weight='bold'), 
        xaxis_tickfont=dict(size=14, family='Ariel , sans-serif', color='#C4C4C4', weight='bold'),
        yaxis_title_font=dict(size=16, family='Ariel , sans-serif', color='#C4C4C4', weight='bold'), 
        yaxis_tickfont=dict(size=14, family='Ariel , sans-serif', color='#C4C4C4', weight='bold'),
        template='plotly_dark',
        transition_duration=500  # Set heatmap transition duration
    )

    return candles, indicator_chart, heatmap


# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)

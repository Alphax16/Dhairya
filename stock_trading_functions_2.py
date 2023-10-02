# stock_trading_functions.py

import yfinance as yf
import pandas as pd


def get_historical_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)
    return data

# def moving_average_crossover_strategy(data, short_window=50, long_window=200):
#     signals = pd.DataFrame(index=data.index)
#     signals['price'] = data['Close']
#     signals['short_mavg'] = data['Close'].rolling(window=short_window, min_periods=1, center=False).mean()
#     signals['long_mavg'] = data['Close'].rolling(window=long_window, min_periods=1, center=False).mean()
#     signals['signal'] = 0.0
#     signals['signal'][short_window:] = signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:]
#     signals['positions'] = signals['signal'].diff()

#     return signals

# def moving_average_crossover_strategy(data, short_window=50, long_window=200):
#     signals = pd.DataFrame(index=data.index)
#     signals['price'] = data['Close']
#     signals['short_mavg'] = data['Close'].rolling(window=short_window, min_periods=1, center=False).mean()
#     signals['long_mavg'] = data['Close'].rolling(window=long_window, min_periods=1, center=False).mean()
#     signals['signal'] = 0.0

#     # Generate signals
#     signals['signal'][short_window:] = (signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:]).astype(int)
#     signals['positions'] = signals['signal'].diff()

#     return signals

def moving_average_crossover_strategy(data, short_window=50, long_window=200):
    signals = pd.DataFrame(index=data.index)
    signals['price'] = data['Close']
    signals['short_mavg'] = data['Close'].rolling(window=short_window, min_periods=1, center=False).mean()
    signals['long_mavg'] = data['Close'].rolling(window=long_window, min_periods=1, center=False).mean()
    signals['signal'] = 0.0
    signals['signal'][short_window:] = (signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:]).astype(int)
    signals['positions'] = signals['signal'].diff()

    # Add short and long moving average columns to the original data DataFrame
    data['Short_MA'] = signals['short_mavg']
    data['Long_MA'] = signals['long_mavg']

    return signals

def predict_stock_prices(data, window=10):
    # Calculate the moving average
    data['Predicted_Close'] = data['Close'].rolling(window=window, min_periods=1).mean()
    return data

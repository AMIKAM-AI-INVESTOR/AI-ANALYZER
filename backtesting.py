
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def fetch_stock_data(symbol, period='6mo', interval='1d'):
    try:
        data = yf.download(symbol, period=period, interval=interval)
        return data
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def generate_signals(data):
    if data is None or data.empty:
        return []

    data['SMA50'] = data['Close'].rolling(window=50).mean()
    data['SMA200'] = data['Close'].rolling(window=200).mean()

    signals = []

    for i in range(1, len(data)):
        if data['SMA50'].iloc[i-1] < data['SMA200'].iloc[i-1] and data['SMA50'].iloc[i] > data['SMA200'].iloc[i]:
            signals.append((data.index[i], data['Close'].iloc[i], 'Buy'))
        elif data['SMA50'].iloc[i-1] > data['SMA200'].iloc[i-1] and data['SMA50'].iloc[i] < data['SMA200'].iloc[i]:
            signals.append((data.index[i], data['Close'].iloc[i], 'Sell'))

    return signals

def plot_signals(data, signals, title=''):
    plt.figure(figsize=(14, 7))
    plt.plot(data.index, data['Close'], label='Close Price', alpha=0.5)
    plt.plot(data.index, data['SMA50'], label='SMA50', linestyle='--')
    plt.plot(data.index, data['SMA200'], label='SMA200', linestyle='--')

    for signal in signals:
        date, price, signal_type = signal
        color = 'green' if signal_type == 'Buy' else 'red'
        plt.scatter(date, price, marker='^' if signal_type == 'Buy' else 'v', color=color, s=100, label=signal_type)

    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig('/mnt/data/backtesting_plot.png')
    plt.close()

# backtesting.py

import matplotlib.pyplot as plt

def run_backtest(data):
    buy_signals = data[data['Signal'] == 'BUY']
    sell_signals = data[data['Signal'] == 'SELL']
    
    plt.figure(figsize=(14, 6))
    plt.plot(data['Date'], data['Close'], label='Close Price', color='blue')
    plt.scatter(buy_signals['Date'], buy_signals['Close'], label='Buy Signal', marker='^', color='green')
    plt.scatter(sell_signals['Date'], sell_signals['Close'], label='Sell Signal', marker='v', color='red')
    plt.title('Backtest of Buy/Sell Signals')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.tight_layout()
    plt.grid(True)
    plt.show()

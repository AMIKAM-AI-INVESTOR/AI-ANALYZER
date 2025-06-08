import yfinance as yf
import pandas as pd
import numpy as np

def fetch_price_history(ticker_symbol, period="6mo", interval="1d"):
    try:
        ticker = yf.Ticker(ticker_symbol)
        hist = ticker.history(period=period, interval=interval)
        return hist
    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {e}")
        return pd.DataFrame()

def detect_trade_signals(df, threshold=0.04):
    df = df.copy()
    df['Signal'] = None

    for i in range(1, len(df) - 1):
        if df['Close'].iloc[i] > df['Close'].iloc[i - 1] * (1 + threshold):
            df.at[df.index[i], 'Signal'] = 'Buy'
        elif df['Close'].iloc[i] < df['Close'].iloc[i - 1] * (1 - threshold):
            df.at[df.index[i], 'Signal'] = 'Sell'

    return df

def calculate_return(df, buy_signal='Buy', sell_signal='Sell'):
    df = df.copy()
    positions = []
    returns = []

    for i in range(len(df)):
        if df['Signal'].iloc[i] == buy_signal:
            positions.append((df.index[i], df['Close'].iloc[i]))
        elif df['Signal'].iloc[i] == sell_signal and positions:
            buy_date, buy_price = positions.pop(0)
            sell_price = df['Close'].iloc[i]
            return_pct = ((sell_price - buy_price) / buy_price) * 100
            returns.append({
                "Buy Date": buy_date,
                "Sell Date": df.index[i],
                "Buy Price": buy_price,
                "Sell Price": sell_price,
                "Return (%)": return_pct
            })

    return pd.DataFrame(returns)

def format_price(value):
    try:
        return f"${value:,.2f}"
    except:
        return value

# utils.py

import matplotlib.pyplot as plt

def plot_price_chart(data):
    buy_signals = data[data['Signal'] == 'BUY']
    sell_signals = data[data['Signal'] == 'SELL']
    
    plt.figure(figsize=(14, 6))
    plt.plot(data['Date'], data['Close'], label='Close Price', color='blue')
    plt.scatter(buy_signals['Date'], buy_signals['Close'], label='Buy Signal', marker='^', color='green')
    plt.scatter(sell_signals['Date'], sell_signals['Close'], label='Sell Signal', marker='v', color='red')
    plt.title('Price Chart with Buy/Sell Signals')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.tight_layout()
    plt.grid(True)
    plt.show()

if data is None or not isinstance(data, pd.DataFrame) or 'signal' not in data.columns:
    st.error("No valid data available for chart.")
    return None

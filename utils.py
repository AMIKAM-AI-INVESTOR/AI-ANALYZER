
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def plot_price_chart(ticker_symbol):
    try:
        data = yf.Ticker(ticker_symbol).history(period="6mo", interval="1d")
        if data.empty or 'Close' not in data.columns:
            return "⚠️ No valid data for plotting."

        data['Signal'] = None
        for i in range(1, len(data) - 1):
            if data['Close'].iloc[i] > data['Close'].iloc[i - 1] * 1.04:
                data.at[data.index[i], 'Signal'] = 'BUY'
            elif data['Close'].iloc[i] < data['Close'].iloc[i - 1] * 0.96:
                data.at[data.index[i], 'Signal'] = 'SELL'

        if 'Signal' not in data.columns:
            return "⚠️ Signal column missing."

        buy_signals = data[data['Signal'] == 'BUY']
        sell_signals = data[data['Signal'] == 'SELL']

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(data.index, data['Close'], label='Close Price', color='blue')
        ax.scatter(buy_signals.index, buy_signals['Close'], label='BUY', color='green', marker='^')
        ax.scatter(sell_signals.index, sell_signals['Close'], label='SELL', color='red', marker='v')
        ax.legend()
        ax.set_title(f"Price chart with signals for {ticker_symbol}")
        return fig

    except Exception as e:
        return f"❌ Chart error: {e}"

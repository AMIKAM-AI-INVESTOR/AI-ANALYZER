
import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import numpy as np
import plotly.graph_objs as go
from datetime import datetime, timedelta

st.set_page_config(page_title="AI Analyzer", layout="wide", page_icon="📈")

st.markdown(
    """
    <style>
    body, .stApp {
        background-color: #111111;
        color: white;
    }
    .stDataFrame table {
        color: white;
        background-color: #222;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True
)

st.title("🚀 AI-Powered Market Analyzer")
ticker = st.text_input("🔢 Enter Symbol (e.g. AAPL, BTC-USD):", "AAPL")

def load_data(symbol):
    end = datetime.today()
    start = end - timedelta(days=365 * 5)
    df = yf.download(symbol, start=start, end=end)
    if df.empty or 'Close' not in df:
        st.error("⚠️ No data found or missing 'Close' column.")
        return None
    df.dropna(inplace=True)

    try:
        close = df['Close'].squeeze()
        df['SMA_50'] = ta.trend.SMAIndicator(close, window=50).sma_indicator()
        df['SMA_200'] = ta.trend.SMAIndicator(close, window=200).sma_indicator()
        df['RSI'] = ta.momentum.RSIIndicator(close, window=14).rsi()
        df['MACD'] = ta.trend.macd_diff(close)
    except Exception as e:
        st.error(f"⚠️ Error during indicator calculation: {e}")
        return None

    return df

def generate_signals(df):
    df['Signal'] = 0
    df.loc[(df['SMA_50'] > df['SMA_200']) & (df['RSI'] < 70), 'Signal'] = 1
    df.loc[(df['SMA_50'] < df['SMA_200']) | (df['RSI'] > 70), 'Signal'] = -1
    return df

def plot_candlestick(df):
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='Candlestick')])

    buy_signals = df[df['Signal'] == 1]
    sell_signals = df[df['Signal'] == -1]

    fig.add_trace(go.Scatter(x=buy_signals.index, y=buy_signals['Close'],
                             mode='markers', marker=dict(color='lime', size=10, symbol='triangle-up'),
                             name='🟢 Buy Signal'))

    fig.add_trace(go.Scatter(x=sell_signals.index, y=sell_signals['Close'],
                             mode='markers', marker=dict(color='red', size=10, symbol='triangle-down'),
                             name='🔴 Sell Signal'))

    fig.update_layout(title="📈 Candlestick Chart with Buy/Sell Signals",
                      xaxis_title="Date", yaxis_title="Price ($)",
                      template="plotly_dark", height=600)
    st.plotly_chart(fig, use_container_width=True)

if ticker:
    df = load_data(ticker)
    if df is not None:
        df = generate_signals(df)
        st.subheader(f"📊 Analysis for: {ticker}")
        signal = df['Signal'].iloc[-1]
        if signal == 1:
            st.success("🟢 BUY recommendation – positive trend detected.")
        elif signal == -1:
            st.error("🔴 SELL recommendation – downward trend detected.")
        else:
            st.warning("⏸️ HOLD – no clear signal detected.")
        plot_candlestick(df)

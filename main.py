
import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import numpy as np
import plotly.graph_objs as go
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="AI Analyzer", layout="wide", page_icon="📈")

# ------------------ STYLING ------------------
st.markdown("""
    <style>
    body, .stApp { background-color: #111111; color: white; }
    .stDataFrame table { color: white; background-color: #222; }
    .stButton>button {
        background-color: #4CAF50; color: white;
        font-weight: bold; border-radius: 10px;
    }
    h1, h2, h3, h4 { color: white; }
    </style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.title("🤖 AI-Powered Market Analyzer")
st.markdown("מערכת המלצות חכמה בזמן אמת על מטבעות ומניות 📈")

# ------------------ INPUT + GRAPH ------------------
ticker = st.text_input("🔎 חפש מניה או מטבע (למשל BTC-USD, ETH-USD, AAPL):", "BTC-USD")

def load_data(symbol):
    end = datetime.today()
    start = end - timedelta(days=365 * 3)
    df = yf.download(symbol, start=start, end=end)
    if df.empty or not all(col in df.columns for col in ['Open', 'High', 'Low', 'Close']):
        return None
    df.dropna(inplace=True)
    try:
        close = df['Close'].squeeze()
        df['SMA_50'] = ta.trend.SMAIndicator(close=close, window=50).sma_indicator()
        df['SMA_200'] = ta.trend.SMAIndicator(close=close, window=200).sma_indicator()
        df['RSI'] = ta.momentum.RSIIndicator(close=close, window=14).rsi()
        df['MACD'] = ta.trend.macd_diff(close)
    except:
        return None
    return df

def generate_signals(df):
    df['Signal'] = 0
    df.loc[(df['SMA_50'] > df['SMA_200']) & (df['RSI'] < 70), 'Signal'] = 1
    df.loc[(df['SMA_50'] < df['SMA_200']) | (df['RSI'] > 70), 'Signal'] = -1
    return df

def plot_candlestick(df):
    fig = go.Figure(data=[go.Candlestick(
        x=df.index, open=df['Open'], high=df['High'],
        low=df['Low'], close=df['Close'], name='Candlestick')])
    buy_signals = df[df['Signal'] == 1]
    sell_signals = df[df['Signal'] == -1]
    fig.add_trace(go.Scatter(x=buy_signals.index, y=buy_signals['Close'],
        mode='markers', marker=dict(color='lime', size=10, symbol='triangle-up'), name='🟢 Buy Signal'))
    fig.add_trace(go.Scatter(x=sell_signals.index, y=sell_signals['Close'],
        mode='markers', marker=dict(color='red', size=10, symbol='triangle-down'), name='🔴 Sell Signal'))
    fig.update_layout(title="📊 גרף נרות יפניים", xaxis_title="תאריך", yaxis_title="מחיר ($)",
                      template="plotly_dark", height=600)
    st.plotly_chart(fig, use_container_width=True)

if ticker:
    df = load_data(ticker)
    if df is not None:
        df = generate_signals(df)
        signal = df['Signal'].iloc[-1]
        st.subheader(f"📈 ניתוח עבור: {ticker}")
        if signal == 1:
            st.success("🟢 המלצה: קנייה")
        elif signal == -1:
            st.error("🔴 המלצה: מכירה")
        else:
            st.warning("⏸️ המתן - אין איתות ברור")
        plot_candlestick(df)
    else:
        st.warning("⚠️ לא ניתן לטעון נתונים")

# ------------------ TOP 10 RECOMMENDATIONS ------------------
def mock_top_assets(asset_type, count=10):
    tickers = {
        "crypto": ["BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "DOGE-USD", "AVAX-USD", "LTC-USD", "BNB-USD", "ADA-USD", "DOT-USD"],
        "stock":  ["AAPL", "NVDA", "TSLA", "AMZN", "MSFT", "PLTR", "PYPL", "META", "QUBT", "SHOP"]
    }
    data = []
    for ticker in tickers[asset_type]:
        current = round(yf.download(ticker, period="1d")["Close"].values[-1], 2)
        change_pct = round(random.uniform(10, 60), 2)
        time_days = random.choice([30, 45, 60, 90])
        future_price = round(current * (1 + change_pct / 100), 2)
        signal = random.choice(["🟢 קנייה", "🔴 מכירה", "⏸️ המתן"])
        data.append({
            "Asset": ticker,
            "Recommendation": signal,
            "Expected Change": f"{change_pct}% → {future_price} $",
            "Target Time": f"{time_days} ימים"
        })
    return pd.DataFrame(data)

col1, col2 = st.columns(2)
with col1:
    st.subheader("🔥 Top 10 Cryptocurrencies")
    st.dataframe(mock_top_assets("crypto"))

with col2:
    st.subheader("📊 Top 10 Stocks")
    st.dataframe(mock_top_assets("stock"))

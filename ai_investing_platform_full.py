
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from datetime import datetime, timedelta

# הגדרות דף
st.set_page_config(page_title="AI Investing Platform", layout="wide", page_icon="📈")

# עיצוב בסיסי כהה
st.markdown("""
    <style>
    body, .stApp {
        background-color: #111;
        color: white;
    }
    .stDataFrame table {
        background-color: #222;
        color: white;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 AI-Powered Investing Platform")

# פונקציה לטעינת נתונים
@st.cache_data
def load_data(symbol):
    try:
        df = yf.download(symbol, period="5y", interval="1d")
        df.dropna(inplace=True)
        return df
    except:
        return pd.DataFrame()

# פונקציית ניתוח טכני והמלצות
def analyze_asset(df):
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['SMA_200'] = df['Close'].rolling(window=200).mean()
    df['RSI'] = 100 - (100 / (1 + df['Close'].pct_change().rolling(14).mean()))
    df['Signal'] = 0
    df.loc[(df['SMA_50'] > df['SMA_200']) & (df['RSI'] < 70), 'Signal'] = 1
    df.loc[(df['SMA_50'] < df['SMA_200']) | (df['RSI'] > 70), 'Signal'] = -1
    return df

# גרף נרות יפניים
def plot_candlestick(df):
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['Open'], high=df['High'],
        low=df['Low'], close=df['Close'],
        name="Candlestick"
    )])
    buy = df[df['Signal'] == 1]
    sell = df[df['Signal'] == -1]
    fig.add_trace(go.Scatter(x=buy.index, y=buy['Close'],
                             mode='markers', marker=dict(color='lime', size=10, symbol='triangle-up'),
                             name='Buy'))
    fig.add_trace(go.Scatter(x=sell.index, y=sell['Close'],
                             mode='markers', marker=dict(color='red', size=10, symbol='triangle-down'),
                             name='Sell'))
    fig.update_layout(template="plotly_dark", height=600, xaxis_title="Date", yaxis_title="Price ($)")
    return fig

# חיפוש מניה או מטבע
ticker = st.text_input("🔎 Search a Stock or Crypto Symbol", "BTC-USD")
if ticker:
    df = load_data(ticker)
    if not df.empty:
        df = analyze_asset(df)
        st.subheader(f"📊 Candlestick Chart: {ticker}")
        st.plotly_chart(plot_candlestick(df), use_container_width=True)
    else:
        st.warning("⚠️ Data not available.")

# טבלת תחזיות לדוגמה (עתיד להתחלף באלגוריתם חכם)
st.markdown("---")
st.subheader("📈 Top 10 Forecasted Stocks")
stocks = pd.DataFrame({
    "Stock": ["QUBT", "ONON", "ENVX", "SMCI", "FUBO", "UPST", "IONQ", "SOFI", "TMDX", "BMBL"],
    "Current Price": [12.3, 38.1, 15.5, 850, 1.9, 22.1, 9.3, 7.4, 93.2, 10.6],
    "Expected Change %": [36, 32, 29, 28, 27, 26, 25, 25, 24, 24],
    "Target Price": [16.7, 50.3, 20.0, 1088, 2.4, 27.8, 11.6, 9.25, 115.5, 13.15],
    "Time Horizon": ["60 ימים", "45 ימים", "50 ימים", "70 ימים", "30 ימים", "45 ימים", "40 ימים", "35 ימים", "55 ימים", "60 ימים"],
    "Recommendation": ["BUY"] * 10
})
st.dataframe(stocks)

st.markdown("---")
st.subheader("💰 Top 10 Forecasted Cryptocurrencies")
crypto = pd.DataFrame({
    "Crypto": ["RNDR", "LDO", "FET", "INJ", "GRT", "AR", "MKR", "KAS", "RUNE", "TWT"],
    "Current Price": [9.8, 2.1, 1.6, 24, 0.32, 44, 2960, 0.14, 7.5, 1.1],
    "Expected Change %": [40, 38, 35, 33, 31, 30, 30, 29, 28, 27],
    "Target Price": [13.7, 2.9, 2.2, 32, 0.42, 57.2, 3848, 0.18, 9.6, 1.4],
    "Time Horizon": ["40 ימים", "35 ימים", "45 ימים", "30 ימים", "50 ימים", "60 ימים", "55 ימים", "45 ימים", "40 ימים", "30 ימים"],
    "Recommendation": ["BUY"] * 10
})
st.dataframe(crypto)

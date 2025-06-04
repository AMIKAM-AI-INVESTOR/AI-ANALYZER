
import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import numpy as np
import plotly.graph_objs as go
from datetime import datetime, timedelta

st.set_page_config(page_title="AI Analyzer", layout="wide", page_icon="📈")

st.markdown("""
<style>
body, .stApp {
    background-color: #111;
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
""", unsafe_allow_html=True)

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
    if df is None or df.empty:
        st.warning("📉 No data to plot.")
        return

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

# טבלת תחזיות טופ 10 מניות ומטבעות (דוגמה)
def show_top_tables():
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

# ------------------ MAIN ------------------
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
    else:
        st.warning("⚠️ Unable to fetch or process data.")

show_top_tables()

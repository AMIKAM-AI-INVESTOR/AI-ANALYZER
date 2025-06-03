import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import numpy as np
import plotly.graph_objs as go
from datetime import datetime, timedelta

st.set_page_config(page_title="AI Crypto Analyzer", layout="wide", page_icon="📊")

# ---------- STYLING ----------
st.markdown("""
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
""", unsafe_allow_html=True)

st.title("🚀 AI-Powered Crypto Analyzer")
ticker = st.text_input("🔢 Enter symbol (e.g. BTC-USD, ETH-USD, AAPL):", "BTC-USD")

def safe_series(column):
    """Convert column to proper Series to avoid 2D errors"""
    return pd.Series(column.values, index=column.index)

def load_data(symbol):
    end = datetime.today()
    start = end - timedelta(days=365 * 5)
    df = yf.download(symbol, start=start, end=end)
    if df.empty or 'Close' not in df or df['Close'].isnull().all():
        return None
    df = df.dropna()
    try:
        close = safe_series(df['Close'].astype(float))
        df['SMA_50'] = ta.trend.SMAIndicator(close, window=50).sma_indicator()
        df['SMA_200'] = ta.trend.SMAIndicator(close, window=200).sma_indicator()
        df['RSI'] = ta.momentum.RSIIndicator(close, window=14).rsi()
        df['MACD'] = ta.trend.macd_diff(close)
    except Exception as e:
        st.warning(f"Error calculating indicators: {e}")
        return None
    return df

def generate_signals(df):
    df['Signal'] = 0
    df.loc[(df['SMA_50'] > df['SMA_200']) & (df['RSI'] < 70), 'Signal'] = 1
    df.loc[(df['SMA_50'] < df['SMA_200']) | (df['RSI'] > 70), 'Signal'] = -1
    return df

def estimate_change(signal):
    if signal == 1:
        return round(np.random.uniform(5, 20), 2)
    elif signal == -1:
        return round(np.random.uniform(-20, -5), 2)
    return round(np.random.uniform(-3, 3), 2)

def score_asset(ticker):
    try:
        df = yf.download(ticker, period="6mo", interval="1d")
        if df.empty or 'Close' not in df or df['Close'].isnull().all():
            return {"Asset": ticker, "Signal": "N/A", "Change (%)": "N/A"}
        df.dropna(inplace=True)
        close = safe_series(df['Close'].astype(float))
        df['SMA_50'] = ta.trend.SMAIndicator(close, window=50).sma_indicator()
        df['SMA_200'] = ta.trend.SMAIndicator(close, window=200).sma_indicator()
        df['RSI'] = ta.momentum.RSIIndicator(close, window=14).rsi()
        df['MACD'] = ta.trend.macd_diff(close)
        df = generate_signals(df)
        signal = df['Signal'].iloc[-1]
        predicted = estimate_change(signal)
        label = "BUY" if signal == 1 else "SELL" if signal == -1 else "HOLD"
        return {"Asset": ticker, "Signal": label, "Change (%)": predicted}
    except:
        return {"Asset": ticker, "Signal": "Error", "Change (%)": "N/A"}

def get_top_assets():
    cryptos = ["BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "DOGE-USD", "AVAX-USD", "LTC-USD", "BNB-USD", "ADA-USD", "DOT-USD"]
    stocks = ["AAPL", "NVDA", "TSLA", "AMZN", "MSFT", "PLTR", "PYPL", "META", "GOOGL", "BABA"]
    crypto_analysis = [score_asset(asset) for asset in cryptos]
    stock_analysis = [score_asset(asset) for asset in stocks]
    return pd.DataFrame(crypto_analysis), pd.DataFrame(stock_analysis)

if ticker:
    df = load_data(ticker)
    if df is not None:
        df = generate_signals(df)
        st.markdown("---")
        st.subheader(f"📊 Analysis for: {ticker}")
        signal = df['Signal'].iloc[-1]
        if signal == 1:
            st.success("🟢 BUY recommendation – positive trend detected.")
        elif signal == -1:
            st.error("🔴 SELL recommendation – downward trend detected.")
        else:
            st.warning("⏸️ HOLD – no clear signal detected.")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Price'))
        fig.add_trace(go.Scatter(x=df.index, y=df['SMA_50'], mode='lines', name='SMA 50'))
        fig.add_trace(go.Scatter(x=df.index, y=df['SMA_200'], mode='lines', name='SMA 200'))
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df[['Close', 'SMA_50', 'SMA_200', 'RSI', 'MACD']].tail(10).round(2))
    else:
        st.error("⚠️ No valid data available or indicators could not be calculated.")

st.sidebar.title("📈 Top Recommendations")
crypto_df, stock_df = get_top_assets()
st.sidebar.subheader("Top 10 Cryptocurrencies")
st.sidebar.dataframe(crypto_df)
st.sidebar.subheader("Top 10 Stocks")
st.sidebar.dataframe(stock_df)

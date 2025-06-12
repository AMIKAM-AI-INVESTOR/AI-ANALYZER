
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
import sys

# Add module path
sys.path.append("/mnt/data")

from top10_data import get_top10_forecasts
from backtesting import run_backtesting
from fundamentals import get_fundamental_data
from utils import detect_trade_signals

st.set_page_config(page_title="AI Analyzer - Stocks & Crypto", layout="wide")

st.title("📊 AI Analyzer - Stocks & Crypto")
st.header("🔍 Analyze a Specific Asset")

# User input for symbol and time range
symbol = st.text_input("Enter a stock or crypto symbol (e.g. AAPL, BTC-USD):", "AAPL")
time_range = st.selectbox("Select time period:", ["1mo", "3mo", "6mo", "1y"])

# Download historical data
@st.cache_data(ttl=3600)
def fetch_data(symbol, period):
    df = yf.download(symbol, period=period)
    return df

df = fetch_data(symbol, time_range)

# Display candlestick chart
st.subheader(f"{symbol.upper()} Candlestick Chart")
if not df.empty and {"Open", "High", "Low", "Close"}.issubset(df.columns):
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"]
    )])
    fig.update_layout(xaxis_title="Date", yaxis_title="Price", xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No valid data found for selected symbol or time range.")

# Run backtesting if data is valid
if not df.empty:
    df = detect_trade_signals(df)
    backtest_df = run_backtesting(df)
    if not backtest_df.empty:
        st.subheader("📊 AI Backtesting Results")
        st.line_chart(backtest_df)

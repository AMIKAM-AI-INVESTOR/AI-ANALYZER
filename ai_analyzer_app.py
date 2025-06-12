
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime, timedelta

from top10_data import get_top10_forecasts
from backtesting import run_backtesting
from fundamentals import get_fundamental_data
from utils import detect_trade_signals

st.set_page_config(layout="wide", page_title="AI Analyzer - Stocks & Crypto")
st.title("📊 AI Analyzer - Stocks & Crypto")

# Section: Top 10 Forecasts
top10_stocks, top10_crypto = get_top10_forecasts()

with st.expander("📈 Top 10 Forecasted Stocks", expanded=True):
    st.dataframe(top10_stocks, use_container_width=True)

with st.expander("🟠 Top 10 Forecasted Cryptocurrencies", expanded=True):
    st.dataframe(top10_crypto, use_container_width=True)

# Section: Analyze a Specific Asset
st.header("🔍 Analyze a Specific Asset")
symbol = st.text_input("Enter a stock or crypto symbol (e.g. AAPL, BTC-USD):", value="AAPL")
period = st.selectbox("Select time period:", ["1mo", "3mo", "6mo", "1y"])

if symbol:
    try:        df = yf.download(symbol, period=period)
        if df.empty:
            st.warning("No data found for this symbol or time range.")
        else:
            df.dropna(inplace=True)
            df = detect_trade_signals(df)

            # Candlestick Chart
            st.subheader(f"{symbol.upper()} Candlestick Chart")
            fig = go.Figure(data=[go.Candlestick(
                x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                increasing_line_color='green',
                decreasing_line_color='red'
            )])
            st.plotly_chart(fig, use_container_width=True)

            # Backtesting
            st.subheader("📉 AI Backtesting Results")
            backtest_df = run_backtesting(df)
            st.line_chart(backtest_df)

            # Fundamentals
            st.subheader("📊 Fundamental Data")
            fundamentals = get_fundamental_data(symbol)
            st.dataframe(fundamentals)


        # Candlestick Chart
        st.subheader(f"{symbol.upper()} Candlestick Chart")
        fig = go.Figure(data=[go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            increasing_line_color='green',
            decreasing_line_color='red'
        )])
        st.plotly_chart(fig, use_container_width=True)

        # Backtesting
        st.subheader("📉 AI Backtesting Results")
        backtest_df = run_backtesting(df)
        st.line_chart(backtest_df)

        # Fundamentals
        st.subheader("📊 Fundamental Data")
        fundamentals = get_fundamental_data(symbol)
        st.dataframe(fundamentals)

    except Exception as e:
        st.error(f"Error loading data: {e}")

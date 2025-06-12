
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils import fetch_price_history, detect_trade_signals
from backtesting import run_backtesting
from fundamentals import get_fundamental_data
from top10_data import load_top10_forecasts

st.set_page_config(layout="wide", page_title="AI Stock & Crypto Analyzer")

st.title("🔍 AI Stock & Crypto Analyzer")

# Load Top 10 Data
stock_forecasts, crypto_forecasts = load_top10_forecasts()

# Display Forecast Tables
st.subheader("📈 Top 10 Stock Forecasts")
st.dataframe(stock_forecasts, use_container_width=True)

st.subheader("📉 Top 10 Crypto Forecasts")
st.dataframe(crypto_forecasts, use_container_width=True)

# Stock/Crypto Symbol Input
st.subheader("🔎 Analyze Specific Asset")
symbol = st.text_input("Enter Stock or Crypto Symbol (e.g., AAPL, TSLA, BTC-USD)", "AAPL")

if symbol:
    try:
        df = fetch_price_history(symbol)

        if df is not None and not df.empty:
            df = detect_trade_signals(df)

            st.subheader("📊 Candlestick Chart with Buy/Sell Signals")
            fig = go.Figure(data=[
                go.Candlestick(
                    x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'],
                    name="Candlestick"
                ),
                go.Scatter(
                    x=df[df['Signal'] == 'Buy'].index,
                    y=df[df['Signal'] == 'Buy']['Close'],
                    mode='markers',
                    marker=dict(symbol='triangle-up', color='green', size=10),
                    name='Buy Signal'
                ),
                go.Scatter(
                    x=df[df['Signal'] == 'Sell'].index,
                    y=df[df['Signal'] == 'Sell']['Close'],
                    mode='markers',
                    marker=dict(symbol='triangle-down', color='red', size=10),
                    name='Sell Signal'
                )
            ])
            fig.update_layout(xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("📚 Fundamental Analysis")
            fundamentals = get_fundamental_data(symbol)
            st.write(fundamentals)

            st.subheader("🔁 Backtesting Performance")
            backtest_result = run_backtesting(df)
            st.write(backtest_result)
        else:
            st.warning("No data available for the selected symbol.")
    except Exception as e:
        st.error(f"An error occurred while fetching data: {e}")

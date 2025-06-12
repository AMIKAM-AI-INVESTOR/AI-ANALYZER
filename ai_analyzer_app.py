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

with st.expander("🪙 Top 10 Forecasted Cryptocurrencies", expanded=True):
    st.dataframe(top10_crypto, use_container_width=True)

# Section: Analyze a Specific Asset
st.header("🔍 Analyze a Specific Asset")
symbol = st.text_input("Enter a stock or crypto symbol (e.g. AAPL, BTC-USD):", value="AAPL")
period = st.selectbox("Select time period:", ["1mo", "3mo", "6mo", "1y"])

if symbol:
    try:
        df = yf.download(symbol, period=period)
        df.dropna(inplace=True)

        if df.empty or not all(col in df.columns for col in ['Open', 'High', 'Low', 'Close']):
            st.warning("No valid data found for selected symbol or time range.")
        else:
            df = detect_trade_signals(df)

            # Candlestick Chart
            st.subheader(f"{symbol.upper()} Candlestick Chart")
            fig = go.Figure(data=[
                go.Candlestick(
                    x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'],
                    name="Price"
                )
            ])

            # Add Buy/Sell signals
            if "Signal" in df.columns:
                buy_signals = df[df['Signal'] == 'Buy']
                sell_signals = df[df['Signal'] == 'Sell']
                fig.add_trace(go.Scatter(x=buy_signals.index, y=buy_signals['Close'],
                                         mode='markers', marker=dict(color='green', size=10),
                                         name='Buy Signal'))
                fig.add_trace(go.Scatter(x=sell_signals.index, y=sell_signals['Close'],
                                         mode='markers', marker=dict(color='red', size=10),
                                         name='Sell Signal'))

            fig.update_layout(xaxis_title="Date", yaxis_title="Price", height=600)
            st.plotly_chart(fig, use_container_width=True)

            # Backtesting Section
            st.subheader("📉 AI Backtesting Results")
            try:
                backtest_df = run_backtesting(df)
                st.line_chart(backtest_df)
            except Exception as e:
                st.error(f"Backtesting Error: {e}")

            # Fundamentals
            st.subheader("📊 Fundamental Data")
            try:
                fund_data = get_fundamental_data(symbol)
                st.dataframe(pd.DataFrame.from_dict(fund_data, orient="index", columns=["Value"]))
            except Exception as e:
                st.error(f"Fundamental Data Error: {e}")

    except Exception as e:
        st.error(f"Error loading data: {e}")

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
        df = df.dropna()
        df['Date'] = df.index
        df.reset_index(drop=True, inplace=True)

        if not df.empty and all(col in df.columns for col in ['Open', 'High', 'Low', 'Close']):
            st.subheader(f"{symbol.upper()} Candlestick Chart")
            fig = go.Figure(data=[
                go.Candlestick(
                    x=df['Date'],
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'],
                    name='Candlestick'
                )
            ])

            df = detect_trade_signals(df)

            # Plot signals
            buy_signals = df[df['Signal'] == 'Buy']
            sell_signals = df[df['Signal'] == 'Sell']

            fig.add_trace(go.Scatter(
                x=buy_signals['Date'],
                y=buy_signals['Close'],
                mode='markers',
                marker=dict(color='green', size=10, symbol='triangle-up'),
                name='Buy'
            ))

            fig.add_trace(go.Scatter(
                x=sell_signals['Date'],
                y=sell_signals['Close'],
                mode='markers',
                marker=dict(color='red', size=10, symbol='triangle-down'),
                name='Sell'
            ))

            fig.update_layout(xaxis_title='Date', yaxis_title='Price')
            st.plotly_chart(fig, use_container_width=True)

            # Backtesting results
            st.subheader("📊 AI Backtesting Results")
            backtest_df = run_backtesting(df)
            if not backtest_df.empty and 'Date' in backtest_df.columns and 'Price' in backtest_df.columns:
                line_fig = go.Figure()
                line_fig.add_trace(go.Scatter(
                    x=backtest_df['Date'],
                    y=backtest_df['Price'],
                    mode='lines',
                    name='Price'
                ))
                st.plotly_chart(line_fig, use_container_width=True)
            else:
                st.warning("Backtesting data is missing or invalid.")
        else:
            st.warning("No valid data available for this asset.")

    except Exception as e:
        st.error(f"An error occurred: {e}")

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objects as go

from utils import fetch_price_history, detect_trade_signals
from fundamentals import get_fundamental_data
from backtesting import run_backtesting
from top10_data import get_top10_forecasts

st.set_page_config(layout="wide", page_title="AI Stock & Crypto Analyzer")

st.title("📈 AI Stock & Crypto Analyzer")

# טבלאות טופ 10 (מניות וקריפטו)
st.subheader("Top 10 Stocks Forecast")
stocks_df = get_top10_predictions("stocks")
st.dataframe(stocks_df, use_container_width=True)

st.subheader("Top 10 Crypto Forecast")
crypto_df = get_top10_predictions("crypto")
st.dataframe(crypto_df, use_container_width=True)

# חיפוש וניתוח נכס
st.subheader("🔎 Analyze Specific Asset")
symbol = st.text_input("Enter a stock or crypto symbol (e.g., AAPL, TSLA, BTC-USD)", "AAPL")
if st.button("Analyze"):
    df = fetch_price_history(symbol)
    if df is not None:
        df = detect_trade_signals(df)

        # גרף נרות עם איתותים
        st.markdown("### Candlestick Chart with Signals")
        fig = go.Figure(data=[
            go.Candlestick(x=df.index, open=df['Open'], high=df['High'],
                           low=df['Low'], close=df['Close'], name='Candlesticks')
        ])
        # סימון איתותים על הגרף
        for i, row in df.iterrows():
            if row['Signal'] == "Buy":
                fig.add_trace(go.Scatter(x=[i], y=[row['Close']], mode='markers',
                                         marker=dict(symbol="arrow-up", color="green", size=10), name="Buy"))
            elif row['Signal'] == "Sell":
                fig.add_trace(go.Scatter(x=[i], y=[row['Close']], mode='markers',
                                         marker=dict(symbol="arrow-down", color="red", size=10), name="Sell"))

        st.plotly_chart(fig, use_container_width=True)

        # ניתוח פנדומנטלי
        st.markdown("### 📊 Fundamental Analysis")
        fundamentals = get_fundamental_data(symbol)
        if fundamentals is not None:
            st.json(fundamentals)
        else:
            st.warning("No fundamental data found.")

        # ביצוע סימולציה של backtesting
        st.markdown("### 🧪 Backtesting")
        bt_result = run_backtesting(df)
        st.write(bt_result)
    else:
        st.error("Failed to retrieve data. Try a different symbol.")

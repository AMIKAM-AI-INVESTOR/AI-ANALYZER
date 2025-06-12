
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

from model_engine import train_ai_model, run_backtesting

st.set_page_config(layout="wide", page_title="AI Analyzer - Stocks & Crypto")

st.title("🔍 Analyze a Specific Asset")

symbol = st.text_input("Enter a stock or crypto symbol (e.g. AAPL, BTC-USD):", value="AAPL")
period = st.selectbox("Select time period:", ["1mo", "3mo", "6mo", "1y", "2y"], index=3)

if symbol:
    df = yf.download(symbol, period=period, interval="1d")

    if not df.empty and all(col in df.columns for col in ["Open", "High", "Low", "Close"]):
        st.subheader(f"{symbol.upper()} Candlestick Chart")

        fig = go.Figure(data=[
            go.Candlestick(
                x=df.index,
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df["Close"]
            )
        ])
        fig.update_layout(height=500, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("📊 AI Backtesting Results")

        model, report = train_ai_model(df.copy())
        backtest_df = run_backtesting(df.copy(), model)
        st.line_chart(backtest_df)

        st.markdown("**Model Accuracy Report:**")
        st.json(report)
    else:
        st.warning("⚠️ Could not retrieve valid candlestick data for the symbol.")

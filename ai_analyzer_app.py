
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from data_fetcher import fetch_price_history
from utils import detect_trade_signals
from top10_data import get_top10_forecasts

st.set_page_config(page_title="AI Analyzer - Stocks & Crypto", layout="wide")
st.title("📊 AI Analyzer - Stocks & Crypto")

# Show Top 10 Forecasts for Stocks and Crypto
st.subheader("📈 Top 10 Forecasted Stocks")
stocks_df, crypto_df = get_top10_forecasts()

if stocks_df is not None:
    st.dataframe(stocks_df)

st.subheader("✅ Top 10 Forecasted Cryptocurrencies")
if crypto_df is not None:
    st.dataframe(crypto_df)

# Analyze a specific asset
st.header("🔍 Analyze a Specific Asset")
symbol = st.text_input("Enter a stock or crypto symbol (e.g. AAPL, BTC-USD):", value="AAPL")
period = st.selectbox("Select time period:", ["1mo", "3mo", "6mo", "1y"])

if symbol:
    df = fetch_price_history(symbol, period=period)
    if df is not None and not df.empty and all(x in df.columns for x in ["Open", "High", "Low", "Close"]):
        df = detect_trade_signals(df)
        st.subheader(f"{symbol.upper()} Candlestick Chart")

        fig = go.Figure(data=[
            go.Candlestick(
                x=df.index,
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df["Close"],
                name="Price",
            )
        ])

        # Buy and Sell Signals
        buy_signals = df[df["Signal"] == "Buy"]
        sell_signals = df[df["Signal"] == "Sell"]

        fig.add_trace(go.Scatter(
            x=buy_signals.index,
            y=buy_signals["Close"],
            mode="markers",
            marker=dict(symbol="arrow-up", color="green", size=10),
            name="Buy Signal"
        ))

        fig.add_trace(go.Scatter(
            x=sell_signals.index,
            y=sell_signals["Close"],
            mode="markers",
            marker=dict(symbol="arrow-down", color="red", size=10),
            name="Sell Signal"
        ))

        fig.update_layout(xaxis_title="Date", yaxis_title="Price", xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No valid data found for this asset. Try another symbol.")

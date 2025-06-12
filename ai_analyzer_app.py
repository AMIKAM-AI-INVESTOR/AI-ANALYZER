
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils import fetch_price_history, detect_trade_signals

st.set_page_config(page_title="AI Analyzer - Stocks & Crypto", layout="wide")
st.title("📊 AI Analyzer - Stocks & Crypto")

# טופס בחירה
symbol = st.text_input("Enter a stock or crypto symbol (e.g. AAPL, BTC-USD):", value="AAPL")
period = st.selectbox("Select time period:", ["1mo", "3mo", "6mo", "1y", "2y"], index=2)

# Top 10 Tables Section
st.subheader("📈 Top 10 Forecasted Stocks")
top10_stocks = pd.DataFrame({
    "Symbol": ["AAPL", "TSLA", "NVDA", "MSFT", "META", "GOOGL", "AMZN", "CRM", "NFLX", "INTC"],
    "Name": ["Apple", "Tesla", "NVIDIA", "Microsoft", "Meta", "Google", "Amazon", "Salesforce", "Netflix", "Intel"],
    "Predicted Change (%)": [8.2, 12.5, 15.3, 5.1, 6.2, 4.9, 7.3, 6.7, 9.1, 5.8],
    "Target Time": ["7d", "5d", "10d", "14d", "12d", "11d", "9d", "8d", "6d", "13d"],
    "Confidence": [0.92, 0.88, 0.93, 0.85, 0.84, 0.83, 0.89, 0.86, 0.91, 0.87],
    "Signal Source": ["Pattern + MA", "Breakout", "Flag", "Volume Spike", "Support", "Triangle", "EMA", "RSI", "Cup", "MACD"]
})
st.dataframe(top10_stocks)

st.subheader("💹 Top 10 Forecasted Cryptos")
top10_cryptos = pd.DataFrame({
    "Symbol": ["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "ADA-USD", "XRP-USD", "DOGE-USD", "DOT-USD", "AVAX-USD", "MATIC-USD"],
    "Name": ["Bitcoin", "Ethereum", "Solana", "BNB", "Cardano", "Ripple", "Dogecoin", "Polkadot", "Avalanche", "Polygon"],
    "Predicted Change (%)": [22.7, 18.9, 27.8, 14.2, 11.4, 9.5, 12.1, 13.3, 15.7, 10.9],
    "Target Time": ["3d", "4d", "3d", "6d", "5d", "7d", "4d", "6d", "5d", "8d"],
    "Confidence": [0.97, 0.95, 0.96, 0.88, 0.85, 0.83, 0.84, 0.86, 0.89, 0.82],
    "Signal Source": ["Momentum", "MACD", "Cup", "Breakout", "Pattern", "RSI", "Volume Spike", "MA Cross", "Flag", "Fib Level"]
})
st.dataframe(top10_cryptos)

# ניתוח מניה או קריפטו נבחר
if symbol:
    try:
        df = fetch_price_history(symbol, period=period)
        df = detect_trade_signals(df)

        if not df.empty:
            # גרף נרות יפניים
            fig = go.Figure(data=[
                go.Candlestick(
                    x=df.index,
                    open=df["Open"],
                    high=df["High"],
                    low=df["Low"],
                    close=df["Close"],
                    name="Candlestick"
                )
            ])

            # סימון Buy/Sell
            for i in range(len(df)):
                if df["Signal"].iloc[i] == "Buy":
                    fig.add_trace(go.Scatter(x=[df.index[i]], y=[df["Close"].iloc[i]],
                                             mode="markers", marker=dict(color="green", size=10),
                                             name="Buy Signal"))
                elif df["Signal"].iloc[i] == "Sell":
                    fig.add_trace(go.Scatter(x=[df.index[i]], y=[df["Close"].iloc[i]],
                                             mode="markers", marker=dict(color="red", size=10),
                                             name="Sell Signal"))

            fig.update_layout(title=f"{symbol} Candlestick Chart", xaxis_title="Date", yaxis_title="Price")
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Recent Data with Signals")
            st.dataframe(df.tail(30))
        else:
            st.warning("⚠️ No data found for this symbol and time period. Try a different one.")

    except Exception as e:
        st.error(f"❌ Error: {e}")


import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils import fetch_price_history, detect_trade_signals

st.set_page_config(page_title="AI Analyzer - Stocks & Crypto", layout="wide")
st.title("📊 AI Analyzer - Stocks & Crypto")

# טופס בחירה
symbol = st.text_input("Enter a stock or crypto symbol (e.g. AAPL, BTC-USD):", value="AAPL")
period = st.selectbox("Select time period:", ["1mo", "3mo", "6mo", "1y", "2y"], index=2)

if symbol:
    try:
        df = fetch_price_history(symbol, period=period)
        df = detect_trade_signals(df)

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

        # טבלת נתונים
        st.subheader("Recent Data with Signals")
        st.dataframe(df.tail(30))

        # טבלת Top 10 (מזויפת בשלב זה - דמו)
        st.subheader("📈 Top 10 Forecasted Stocks & Cryptos")
        demo_top10 = pd.DataFrame({
            "Symbol": ["AAPL", "TSLA", "NVDA", "MSFT", "BTC-USD", "ETH-USD", "META", "GOOGL", "SOL-USD", "AMZN"],
            "Name": ["Apple", "Tesla", "NVIDIA", "Microsoft", "Bitcoin", "Ethereum", "Meta", "Google", "Solana", "Amazon"],
            "Predicted Change (%)": [8.2, 12.5, 15.3, 5.1, 22.7, 18.9, 6.2, 4.9, 27.8, 7.3],
            "Target Time": ["7d", "5d", "10d", "14d", "3d", "4d", "12d", "11d", "3d", "9d"],
            "Confidence Score": [0.92, 0.88, 0.93, 0.85, 0.97, 0.95, 0.84, 0.83, 0.96, 0.89],
            "Signal Source": ["Pattern + MA", "Breakout", "Flag", "Volume Spike", "Momentum", "MACD", "Support", "Triangle", "Cup", "EMA"]
        })
        st.dataframe(demo_top10)

    except Exception as e:
        st.error(f"❌ Error: {e}")

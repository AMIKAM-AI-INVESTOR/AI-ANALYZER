import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ייבוא הפונקציות מקובץ utils
from utils import fetch_price_history, detect_trade_signals

# כותרת האפליקציה
st.set_page_config(page_title="AI Stock & Crypto Analyzer", layout="wide")
st.title("📊 AI Analyzer - Stocks & Crypto")

# בחירת נכס
symbol = st.text_input("Enter a stock or crypto symbol (e.g. AAPL, BTC-USD):", value="AAPL")

# טווח זמן
period = st.selectbox("Select time period:", ["1mo", "3mo", "6mo", "1y", "2y"], index=2)

# שליפת נתונים
if symbol:
    with st.spinner("Fetching data..."):
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

        # הוספת סימני קנייה/מכירה
        for i in range(len(df)):
            if df["Signal"].iloc[i] == "Buy":
                fig.add_trace(go.Scatter(x=[df.index[i]], y=[df["Close"].iloc[i]],
                                         mode="markers", marker=dict(color="green", size=10),
                                         name="Buy Signal"))
            elif df["Signal"].iloc[i] == "Sell":
                fig.add_trace(go.Scatter(x=[df.index[i]], y=[df["Close"].iloc[i]],
                                         mode="markers", marker=dict(color="red", size=10),
                                         name="Sell Signal"))

        fig.update_layout(title=f"Candlestick Chart for {symbol}", xaxis_title="Date", yaxis_title="Price")
        st.plotly_chart(fig, use_container_width=True)

        # הצגת טבלה
        st.subheader("Raw Data with Signals")
        st.dataframe(df.tail(50))

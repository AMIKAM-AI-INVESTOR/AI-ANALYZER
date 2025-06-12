
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from utils import detect_trade_signals

st.set_page_config(page_title="AI Analyzer - Stocks & Crypto", layout="wide")
st.title("📊 AI Analyzer - Stocks & Crypto")

@st.cache_data
def fetch_price_history(symbol, period="6mo"):
    try:
        data = yf.download(tickers=symbol, period=period, interval="1d", progress=False)
        if data.empty:
            return None
        data = data[["Open", "High", "Low", "Close"]] if all(col in data.columns for col in ["Open", "High", "Low", "Close"]) else None
        return data
    except Exception:
        return None

# Analyze Section
st.markdown("## 🔍 Analyze a Specific Asset")
symbol = st.text_input("Enter a stock or crypto symbol (e.g. AAPL, BTC-USD):", value="AAPL")
period = st.selectbox("Select time period:", ["1mo", "3mo", "6mo", "1y", "2y"], index=2)

if symbol:
    df = fetch_price_history(symbol, period=period)

    if df is None:
        st.warning("⚠️ Data unavailable or missing essential columns (Open, High, Low, Close).")
    else:
        df.index = pd.to_datetime(df.index)
        df = detect_trade_signals(df)
        for col in ["Open", "High", "Low", "Close"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        df = df.dropna(subset=["Open", "High", "Low", "Close"])
        if df.empty:
            st.warning("⚠️ Not enough valid data to render candlestick chart.")
        else:
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
            for i in range(len(df)):
                if df["Signal"].iloc[i] == "Buy":
                    fig.add_trace(go.Scatter(x=[df.index[i]], y=[df["Close"].iloc[i]],
                                             mode="markers", marker=dict(color="green", size=10),
                                             name="Buy Signal"))
                elif df["Signal"].iloc[i] == "Sell":
                    fig.add_trace(go.Scatter(x=[df.index[i]], y=[df["Close"].iloc[i]],
                                             mode="markers", marker=dict(color="red", size=10),
                                             name="Sell Signal"))
            fig.update_layout(title=f"{symbol.upper()} Candlestick Chart", xaxis_title="Date", yaxis_title="Price")
            st.plotly_chart(fig, use_container_width=True)

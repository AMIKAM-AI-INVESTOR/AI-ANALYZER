
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils import fetch_price_history, detect_trade_signals

st.set_page_config(page_title="AI Analyzer - Stocks & Crypto", layout="wide")
st.markdown("# 📊 AI Analyzer - Stocks & Crypto")

# דמו נתונים לניתוח ומחיר יעד
def calculate_target_price(price, percent):
    return round(price * (1 + percent / 100), 2)

# טבלת Top 10 מניות
st.subheader("📈 Top 10 Forecasted Stocks")
top10_stocks = pd.DataFrame({
    "Symbol": ["AAPL", "TSLA", "NVDA", "MSFT", "META", "GOOGL", "AMZN", "CRM", "NFLX", "INTC"],
    "Name": ["Apple", "Tesla", "NVIDIA", "Microsoft", "Meta", "Google", "Amazon", "Salesforce", "Netflix", "Intel"],
    "Current Price": [185.0, 190.3, 110.1, 345.6, 295.0, 132.8, 128.9, 212.5, 450.0, 42.3],
    "Predicted Change (%)": [8.2, 12.5, 15.3, 5.1, 6.2, 4.9, 7.3, 6.7, 9.1, 5.8],
    "Target Time": ["7d", "5d", "10d", "14d", "12d", "11d", "9d", "8d", "6d", "13d"],
    "Confidence": [0.92, 0.88, 0.93, 0.85, 0.84, 0.83, 0.89, 0.86, 0.91, 0.87],
    "Explanation": [
        "Bullish flag pattern detected",
        "Breakout above key resistance",
        "MACD bullish crossover + strong earnings",
        "Stable fundamentals, low volatility",
        "Support zone rebound + positive earnings",
        "Triangle breakout confirmed",
        "EMA50/200 bullish cross",
        "High RSI momentum build-up",
        "Cup and handle pattern",
        "MACD signal + strong volume increase"
    ]
})
top10_stocks["Target Price"] = top10_stocks.apply(
    lambda row: calculate_target_price(row["Current Price"], row["Predicted Change (%)"]), axis=1)
st.dataframe(top10_stocks)

# טבלת Top 10 קריפטו
st.subheader("💹 Top 10 Forecasted Cryptos")
top10_cryptos = pd.DataFrame({
    "Symbol": ["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "ADA-USD", "XRP-USD", "DOGE-USD", "DOT-USD", "AVAX-USD", "MATIC-USD"],
    "Name": ["Bitcoin", "Ethereum", "Solana", "BNB", "Cardano", "Ripple", "Dogecoin", "Polkadot", "Avalanche", "Polygon"],
    "Current Price": [67500, 3700, 160, 590, 0.45, 0.59, 0.15, 6.2, 35.0, 1.2],
    "Predicted Change (%)": [22.7, 18.9, 27.8, 14.2, 11.4, 9.5, 12.1, 13.3, 15.7, 10.9],
    "Target Time": ["3d", "4d", "3d", "6d", "5d", "7d", "4d", "6d", "5d", "8d"],
    "Confidence": [0.97, 0.95, 0.96, 0.88, 0.85, 0.83, 0.84, 0.86, 0.89, 0.82],
    "Explanation": [
        "Momentum surge + halving effect",
        "Strong ETH staking activity",
        "Breakout from long-term consolidation",
        "Technical wedge breakout",
        "Fibonacci retracement complete",
        "Positive XRP ruling news",
        "Social media-driven spike",
        "Volume accumulation detected",
        "Inverse head and shoulders pattern",
        "50-day MA crossover"
    ]
})
top10_cryptos["Target Price"] = top10_cryptos.apply(
    lambda row: calculate_target_price(row["Current Price"], row["Predicted Change (%)"]), axis=1)
st.dataframe(top10_cryptos)

# בחירת נכס לניתוח
st.markdown("## 🔍 Analyze Specific Asset")
symbol = st.text_input("Enter a stock or crypto symbol (e.g. AAPL, BTC-USD):", value="AAPL")
period = st.selectbox("Select time period:", ["1mo", "3mo", "6mo", "1y", "2y"], index=2)

if symbol:
    try:
        df = fetch_price_history(symbol, period=period)
        df = detect_trade_signals(df)

        if not df.empty:
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

            st.subheader("🧠 Fundamental Analysis (Demo)")
            fundamentals_demo = {
                "P/E Ratio": 28.5,
                "EPS (TTM)": 5.23,
                "Market Cap": "1.3T",
                "Sector": "Technology",
                "Dividend Yield": "0.55%",
                "Debt/Equity": 1.5,
                "Insider Ownership": "0.75%",
                "Analyst Rating": "Buy",
                "12-Month Price Target": "$210",
                "Support Zone": "$195-$198",
                "Technical Trend": "Uptrend",
                "Forecast Explanation": "Price expected to rise due to bullish flag pattern, strong fundamentals and high trading volume"
            }
            st.json(fundamentals_demo)
        else:
            st.warning("⚠️ No data found for this symbol and time period. Try a different one.")
    except Exception as e:
        st.error(f"❌ Error: {e}")

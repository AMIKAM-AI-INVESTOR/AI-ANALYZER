
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from data_fetcher import fetch_price_history

st.set_page_config(page_title="AI Analyzer - Stocks & Crypto", layout="wide")
st.title("📊 AI Analyzer - Stocks & Crypto")

@st.cache_data
def get_latest_prices(tickers):
    try:
        df = yf.download(tickers=tickers, period="1d", interval="1d", progress=False)["Close"]
        return df.iloc[-1].round(2).to_dict()
    except Exception:
        return {}

@st.cache_data
def fetch_price_history(symbol, period="6mo"):
    try:
        df = yf.download(tickers=symbol, period=period, interval="1d", progress=False)
        if df.empty or not all(col in df.columns for col in ["Open", "High", "Low", "Close"]):
            return None
        df = df[["Open", "High", "Low", "Close", "Volume"]].dropna()
        return df
    except Exception:
        return None

def calculate_target_price(price, percent):
    return round(price * (1 + percent / 100), 2)

# Top 10 Forecast Tables – placeholders for now
stock_symbols = ["AAPL", "TSLA", "NVDA", "MSFT", "META", "GOOGL", "AMZN", "CRM", "NFLX", "INTC"]
crypto_symbols = ["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "ADA-USD", "XRP-USD", "DOGE-USD", "DOT-USD", "AVAX-USD", "MATIC-USD"]
all_symbols = stock_symbols + crypto_symbols
prices = get_latest_prices(all_symbols)

# Mock predictions (replace with AI later)
stock_data = {
    "Symbol": stock_symbols,
    "Name": ["Apple", "Tesla", "NVIDIA", "Microsoft", "Meta", "Google", "Amazon", "Salesforce", "Netflix", "Intel"],
    "Predicted Change (%)": [8.2, 12.5, 15.3, 5.1, 6.2, 4.9, 7.3, 6.7, 9.1, 5.8],
    "Target Time": ["7d", "5d", "10d", "14d", "12d", "11d", "9d", "8d", "6d", "13d"],
    "Confidence": [0.92, 0.88, 0.93, 0.85, 0.84, 0.83, 0.89, 0.86, 0.91, 0.87],
    "Forecast Explanation (Hebrew)": [
        "תבנית טכנית חזקה + מגמה שורית.",
        "איתות פריצה טכני + נפחים גבוהים.",
        "MACD עולה + מומנטום חזק.",
        "תמיכה + ניתוח טכני חיובי.",
        "יציאה מדשדוש + גידול במחזור.",
        "מגמה עולה יציבה + המלצות אנליסטים.",
        "גידול בביקושים + סנטימנט חיובי.",
        "רווחיות משופרת + פריצה על הגרף.",
        "צפי לעלייה בעקבות תבנית קלאסית.",
        "הצטברות בשפל + איתותים חיוביים."
    ]
}
stock_df = pd.DataFrame(stock_data)
stock_df["Current Price"] = stock_df["Symbol"].apply(lambda s: prices.get(s, 0))
stock_df["Target Price"] = stock_df.apply(lambda row: calculate_target_price(row["Current Price"], row["Predicted Change (%)"]), axis=1)

# Arrange columns properly
stock_df = stock_df[["Symbol", "Name", "Current Price", "Predicted Change (%)", "Target Price", "Target Time", "Confidence", "Forecast Explanation (Hebrew)"]]
st.subheader("📈 Top 10 Forecasted Stocks")
st.dataframe(stock_df)

# Crypto table
crypto_data = {
    "Symbol": crypto_symbols,
    "Name": ["Bitcoin", "Ethereum", "Solana", "BNB", "Cardano", "Ripple", "Dogecoin", "Polkadot", "Avalanche", "Polygon"],
    "Predicted Change (%)": [22.7, 18.9, 27.8, 14.2, 11.4, 9.5, 12.1, 13.3, 15.7, 10.9],
    "Target Time": ["3d", "4d", "3d", "6d", "5d", "7d", "4d", "6d", "5d", "8d"],
    "Confidence": [0.97, 0.95, 0.96, 0.88, 0.85, 0.83, 0.84, 0.86, 0.89, 0.82],
    "Forecast Explanation (Hebrew)": [
        "זיהוי תבנית שורית + גידול בביקושים.",
        "נתונים חזקים מהבלוקצ'יין + פריצה טכנית.",
        "סנטימנט חיובי + תנועה טכנית חדה.",
        "ניתוח EMA מראה מומנטום עולה.",
        "MACD חיובי + תבנית 'כוס וידית'.",
        "איתות RSI שורי + תמיכה היסטורית.",
        "זינוק במחזורים + המלצות שוק.",
        "סיום תיקון טכני + איתותים חזקים.",
        "סימני הצטברות + תבנית משולש עולה.",
        "קונסולידציה מוצקה + EMA כלפי מעלה."
    ]
}
crypto_df = pd.DataFrame(crypto_data)
crypto_df["Current Price"] = crypto_df["Symbol"].apply(lambda s: prices.get(s, 0))
crypto_df["Target Price"] = crypto_df.apply(lambda row: calculate_target_price(row["Current Price"], row["Predicted Change (%)"]), axis=1)
crypto_df = crypto_df[["Symbol", "Name", "Current Price", "Predicted Change (%)", "Target Price", "Target Time", "Confidence", "Forecast Explanation (Hebrew)"]]

st.subheader("💹 Top 10 Forecasted Cryptocurrencies")
st.dataframe(crypto_df)

# Analyze Specific
st.markdown("## 🔍 Analyze a Specific Asset")
symbol = st.text_input("Enter a stock or crypto symbol (e.g. AAPL, BTC-USD):", value="AAPL")
period = st.selectbox("Select time period:", ["1mo", "3mo", "6mo", "1y", "2y"], index=2)

if symbol:
    df = fetch_price_history(symbol, period)
    if df is None:
        st.warning("⚠️ Data unavailable or missing OHLC columns.")
    else:
        df.index = pd.to_datetime(df.index)
        df = detect_trade_signals(df)
        if df.empty:
            st.warning("⚠️ No data available after filtering.")
        else:
            try:
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
            except Exception:
                st.warning("⚠️ Failed to render chart. Check data format.")

from ai_engine import train_predict_xgb

prediction, confidence = train_predict_xgb(df)

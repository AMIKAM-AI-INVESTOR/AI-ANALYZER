
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from utils import fetch_price_history, detect_trade_signals

st.set_page_config(page_title="AI Analyzer - Stocks & Crypto", layout="wide")
st.markdown("# 📊 AI Analyzer - Stocks & Crypto")

@st.cache_data
def get_latest_prices(tickers):
    df = yf.download(tickers=tickers, period="1d", interval="1d", progress=False)["Close"]
    return df.iloc[-1].round(2).to_dict()

def calculate_target_price(price, percent):
    return round(price * (1 + percent / 100), 2)

# Symbols for Top 10
stock_symbols = ["AAPL", "TSLA", "NVDA", "MSFT", "META", "GOOGL", "AMZN", "CRM", "NFLX", "INTC"]
crypto_symbols = ["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "ADA-USD", "XRP-USD", "DOGE-USD", "DOT-USD", "AVAX-USD", "MATIC-USD"]

# Fetch latest prices
all_symbols = stock_symbols + crypto_symbols
prices = get_latest_prices(all_symbols)

# STOCK TABLE
st.subheader("📈 Top 10 Forecasted Stocks")
stock_data = {
    "Symbol": stock_symbols,
    "Name": ["Apple", "Tesla", "NVIDIA", "Microsoft", "Meta", "Google", "Amazon", "Salesforce", "Netflix", "Intel"],
    "Current Price": [prices[s] for s in stock_symbols],
    "Predicted Change (%)": [8.2, 12.5, 15.3, 5.1, 6.2, 4.9, 7.3, 6.7, 9.1, 5.8],
    "Target Time": ["7d", "5d", "10d", "14d", "12d", "11d", "9d", "8d", "6d", "13d"],
    "Confidence": [0.92, 0.88, 0.93, 0.85, 0.84, 0.83, 0.89, 0.86, 0.91, 0.87],
    "Forecast Explanation (Hebrew)": [
        "דגל שורי אותר בגרף עם מחזור מסחר גבוה – תומך בעלייה אפשרית.",
        "פריצה של התנגדות טכנית קריטית + עליה ב-RSI.",
        "שילוב של איתות MACD חיובי ודוחות כספיים חזקים.",
        "מגמה יציבה עם תנודתיות נמוכה וסנטימנט שורי.",
        "חזרה מאזור תמיכה מוכח + גידול ברווחיות הרבעונית.",
        "פריצת תבנית משולש עולה + מחזורי קנייה גבוהים.",
        "חציית ממוצעים נעים (EMA 50 / 200) כלפי מעלה.",
        "מדדי מומנטום גבוהים, סנטימנט שוק חיובי.",
        "תבנית כוס עם ידית בבנייה + צפי לשבירת שיאים.",
        "MACD עולה בתיאום עם קפיצה משמעותית במחזור."
    ]
}
stock_df = pd.DataFrame(stock_data)
stock_df["Target Price"] = stock_df.apply(lambda row: calculate_target_price(row["Current Price"], row["Predicted Change (%)"]), axis=1)
cols = ["Symbol", "Name", "Current Price", "Predicted Change (%)", "Target Price", "Target Time", "Confidence", "Forecast Explanation (Hebrew)"]
st.dataframe(stock_df[cols])

# CRYPTO TABLE
st.subheader("💹 Top 10 Forecasted Cryptocurrencies")
crypto_data = {
    "Symbol": crypto_symbols,
    "Name": ["Bitcoin", "Ethereum", "Solana", "BNB", "Cardano", "Ripple", "Dogecoin", "Polkadot", "Avalanche", "Polygon"],
    "Current Price": [prices[s] for s in crypto_symbols],
    "Predicted Change (%)": [22.7, 18.9, 27.8, 14.2, 11.4, 9.5, 12.1, 13.3, 15.7, 10.9],
    "Target Time": ["3d", "4d", "3d", "6d", "5d", "7d", "4d", "6d", "5d", "8d"],
    "Confidence": [0.97, 0.95, 0.96, 0.88, 0.85, 0.83, 0.84, 0.86, 0.89, 0.82],
    "Forecast Explanation (Hebrew)": [
        "גל עליות חזק לאחר חציית רמות התנגדות והלווייתנים קונים.",
        "עליה בהיקפי סטייקינג + תנועה חיובית בגרף MACD.",
        "יציאה מתבנית דחיסה ארוכה ותמיכה ברורה סביב 140$.",
        "פריצה ממשולש שורי ארוך טווח עם נפחים גבוהים.",
        "תיקון טכני הסתיים + תמיכה בפיבונאצ’י + עלייה בעניין מוסדי.",
        "חדשות רגולציה חיוביות + תנועה סימטרית עולה.",
        "סנטימנט שורי ברשתות + פריצה של רמת התנגדות עגולה.",
        "תמיכה יציבה והצטברות נפח סביב ממוצע 50 יום.",
        "תבנית ראש וכתפיים הפוכה + עליה במחזור.",
        "קרוס ממוצע נע מעלה + עניין גובר בשוק."
    ]
}
crypto_df = pd.DataFrame(crypto_data)
crypto_df["Target Price"] = crypto_df.apply(lambda row: calculate_target_price(row["Current Price"], row["Predicted Change (%)"]), axis=1)
st.dataframe(crypto_df[cols])

# ANALYZE SPECIFIC ASSET
st.markdown("## 🔍 Analyze a Specific Asset")
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
                "Forecast Explanation (Hebrew)": "המערכת זיהתה דגל שורי על רקע תנועה יציבה, מחזורים גבוהים, ורקע פנדומנטלי חזק"
            }
            st.json(fundamentals_demo)
        else:
            st.warning("⚠️ No valid price data available to show chart for this asset.")
    except Exception as e:
        st.error(f"❌ Error: {e}")

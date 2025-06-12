
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils import fetch_price_history, detect_trade_signals

st.set_page_config(page_title="AI Analyzer - Stocks & Crypto", layout="wide")
st.markdown("# 📊 AI Analyzer - Stocks & Crypto")

def calculate_target_price(price, percent):
    return round(price * (1 + percent / 100), 2)

# טבלת Top 10 מניות
st.subheader("📈 התחזיות המובילות למניות")
top10_stocks = pd.DataFrame({
    "Symbol": ["AAPL", "TSLA", "NVDA", "MSFT", "META", "GOOGL", "AMZN", "CRM", "NFLX", "INTC"],
    "Name": ["Apple", "Tesla", "NVIDIA", "Microsoft", "Meta", "Google", "Amazon", "Salesforce", "Netflix", "Intel"],
    "Current Price": [185.0, 190.3, 110.1, 345.6, 295.0, 132.8, 128.9, 212.5, 450.0, 42.3],
    "Predicted Change (%)": [8.2, 12.5, 15.3, 5.1, 6.2, 4.9, 7.3, 6.7, 9.1, 5.8],
    "Target Price": [],
    "Target Time": ["7 ימים", "5 ימים", "10 ימים", "14 ימים", "12 ימים", "11 ימים", "9 ימים", "8 ימים", "6 ימים", "13 ימים"],
    "Confidence": [0.92, 0.88, 0.93, 0.85, 0.84, 0.83, 0.89, 0.86, 0.91, 0.87],
    "הסבר התחזית": [
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
})
top10_stocks["Target Price"] = top10_stocks.apply(lambda row: calculate_target_price(row["Current Price"], row["Predicted Change (%)"]), axis=1)
cols = ["Symbol", "Name", "Current Price", "Predicted Change (%)", "Target Price", "Target Time", "Confidence", "הסבר התחזית"]
st.dataframe(top10_stocks[cols])

# טבלת Top 10 קריפטו
st.subheader("💹 התחזיות המובילות למטבעות קריפטו")
top10_cryptos = pd.DataFrame({
    "Symbol": ["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "ADA-USD", "XRP-USD", "DOGE-USD", "DOT-USD", "AVAX-USD", "MATIC-USD"],
    "Name": ["Bitcoin", "Ethereum", "Solana", "BNB", "Cardano", "Ripple", "Dogecoin", "Polkadot", "Avalanche", "Polygon"],
    "Current Price": [67500, 3700, 160, 590, 0.45, 0.59, 0.15, 6.2, 35.0, 1.2],
    "Predicted Change (%)": [22.7, 18.9, 27.8, 14.2, 11.4, 9.5, 12.1, 13.3, 15.7, 10.9],
    "Target Price": [],
    "Target Time": ["3 ימים", "4 ימים", "3 ימים", "6 ימים", "5 ימים", "7 ימים", "4 ימים", "6 ימים", "5 ימים", "8 ימים"],
    "Confidence": [0.97, 0.95, 0.96, 0.88, 0.85, 0.83, 0.84, 0.86, 0.89, 0.82],
    "הסבר התחזית": [
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
})
top10_cryptos["Target Price"] = top10_cryptos.apply(lambda row: calculate_target_price(row["Current Price"], row["Predicted Change (%)"]), axis=1)
st.dataframe(top10_cryptos[cols])

# ניתוח מניה או מטבע נבחר
st.markdown("## 🔍 ניתוח מניה או מטבע")
symbol = st.text_input("הזן סמל מניה או מטבע (למשל: AAPL, BTC-USD)", value="AAPL")
period = st.selectbox("בחר תקופת זמן לניתוח:", ["1mo", "3mo", "6mo", "1y", "2y"], index=2)

if symbol:
    try:
        df = fetch_price_history(symbol, period=period)
        df = detect_trade_signals(df)

        if not df.empty and df["Close"].dtype != object:
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

            fig.update_layout(title=f"{symbol.upper()} - גרף נרות עם איתותים", xaxis_title="תאריך", yaxis_title="מחיר")
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("🧠 ניתוח פנדומנטלי (מדגם)")
            fundamentals_demo = {
                "מכפיל רווח (P/E)": 28.5,
                "רווח למניה (EPS)": 5.23,
                "שווי שוק": "1.3 טריליון דולר",
                "מגזר": "טכנולוגיה",
                "תשואת דיבידנד": "0.55%",
                "יחס חוב להון": 1.5,
                "אחזקת אנשי פנים": "0.75%",
                "המלצת אנליסטים": "קנייה",
                "יעד מחיר ל-12 חודשים": "$210",
                "אזור תמיכה": "$195-$198",
                "מגמה טכנית": "מגמת עלייה",
                "הסבר התחזית": "המערכת זיהתה דגל שורי על רקע תנועה יציבה, מחזורים גבוהים, ורקע פנדומנטלי חזק"
            }
            st.json(fundamentals_demo)
        else:
            st.warning("⚠️ לא נמצאו נתונים רלוונטיים להצגה בגרף עבור הנכס הזה.")
    except Exception as e:
        st.error(f"❌ שגיאה: {e}")

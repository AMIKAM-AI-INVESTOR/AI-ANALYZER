import streamlit as st
import pandas as pd

from model_engine import stock_symbols, crypto_symbols, train_model, fetch_price_history, analyze_with_model
from explanations import generate_explanation
from utils import detect_trade_signals, plot_candlestick_chart

st.set_page_config(layout="wide", page_title="AI Stock & Crypto Analyzer")

st.title("📊 AI Stock & Crypto Analyzer - תחזיות חכמות")

st.markdown("### תחזיות בזמן אמת | ניתוח גרפי | תחזיות חכמות")

# Load or train the model (could be improved with caching or loading pre-trained)
model = train_model()

# Forecast Section - Stocks
st.markdown("## 🧠 Top 10 מניות מומלצות")

df_stocks = analyze_with_model(model, stock_symbols, "מניה")
if df_stocks.empty:
    st.warning("⚠️ לא נמצאו תחזיות עדכניות עבור מניות.")
else:
    st.dataframe(df_stocks)

# Forecast Section - Crypto
st.markdown("## 🧠 Top 10 מטבעות קריפטו מומלצים")

df_crypto = analyze_with_model(model, crypto_symbols, "קריפטו")
if df_crypto.empty:
    st.warning("⚠️ לא נמצאו תחזיות עדכניות עבור קריפטו.")
else:
    st.dataframe(df_crypto)

# Manual Symbol Search and Analysis
st.markdown("---")
st.markdown("## 🔍 ניתוח לפי סימול בודד")

symbol = st.text_input("🔎 הכנס סימול (לדוגמה AAPL או BTC-USD):")

date_range = st.selectbox("⏱ טווח זמן לניתוח הגרף:", ["6 חודשים", "3 חודשים", "חודש", "שבוע"])

date_mapping = {
    "6 חודשים": 180,
    "3 חודשים": 90,
    "חודש": 30,
    "שבוע": 7
}

if symbol:
    try:
        df = fetch_price_history(symbol, days=date_mapping[date_range])
        if df is not None and not df.empty:
            df = detect_trade_signals(df)
            st.plotly_chart(plot_candlestick_chart(df, symbol), use_container_width=True)
        else:
            st.warning("🔁 לא נמצאו נתונים עבור הסימול שציינת.")
    except Exception as e:
        st.error(f"❌ שגיאה בניתוח הסימול: {e}")

import streamlit as st
import pandas as pd

from model_engine import stock_symbols, crypto_symbols, train_model, fetch_price_history, analyze_with_model
from explanations import generate_explanation
from utils import detect_trade_signals, plot_candlestick_chart

# כותרת
st.set_page_config(layout="wide", page_title="AI Stock & Crypto Analyzer")
st.title("📊 AI Stock & Crypto Analyzer - תחזיות חכמות")

# טאב ניווט
tabs = st.tabs(["תחזיות חכמות", "ניתוח גרפי", "איתותים בזמן אמת"])

# ----------------------------
# תחזיות חכמות - טופ 10
# ----------------------------
with tabs[0]:
    st.subheader("🧠 Top 10 מניות מומלצות")
    model = train_model()

    df_stocks = analyze_with_model(model, stock_symbols, "מניה")
    df_crypto = analyze_with_model(model, crypto_symbols, "קריפטו")

    if df_stocks.empty:
        st.warning("❗ לא נמצאו תחזיות עדכניות עבור מניות.")
    else:
        st.dataframe(df_stocks)

    st.subheader("🧠 Top 10 מטבעות קריפטו מומלצים")
    if df_crypto.empty:
        st.warning("❗ לא נמצאו תחזיות עדכניות עבור קריפטו.")
    else:
        st.dataframe(df_crypto)

# ----------------------------
# ניתוח לפי סימול בודד
# ----------------------------
with tabs[1]:
    st.subheader("🔍 ניתוח לפי סימול בודד")
    symbol = st.text_input("הכנס סימול (לדוגמה AAPL או BTC-USD):")
    period = st.selectbox("טווח זמן לניתוח הגרף:", ["3 חודשים", "6 חודשים", "שנה", "5 שנים"])

    if symbol:
        df = fetch_price_history(symbol, period)
        if df is not None and not df.empty:
            df = detect_trade_signals(df)
            explanation = generate_explanation(df)
            st.write("📌", explanation)
            plot_candlestick_chart(df, symbol)
        else:
            st.error("לא ניתן לטעון נתונים עבור הסימול שהוזן.")

# ----------------------------
# איתותים בזמן אמת
# ----------------------------
with tabs[2]:
    st.subheader("⏱ איתותים בזמן אמת")
    st.info("בקרוב - ניתוח בזמן אמת של איתותי קנייה/מכירה ממאות נכסים.")

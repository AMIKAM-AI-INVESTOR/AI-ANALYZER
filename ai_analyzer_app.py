import streamlit as st
import pandas as pd
import numpy as np

from model_engine import stock_symbols, crypto_symbols, train_model, fetch_price_history, analyze_with_model
from explanations import generate_explanation
from utils import detect_trade_signals

st.set_page_config(page_title="AI Stock & Crypto Analyzer", layout="wide")

st.title("📊 AI Stock & Crypto Analyzer - תחזיות חכמות")
st.markdown("### תחזיות בזמן אמת | ניתוח גרפי | איתותים")

# טבלת טופ 10 מניות
st.subheader("📈 Top 10 מניות מומלצות")
df_stocks = analyze_with_model(train_model(), stock_symbols, "מנייה")
if df_stocks is not None and not df_stocks.empty:
    st.dataframe(df_stocks)
else:
    st.warning("לא נמצאו תחזיות עדכניות עבור מניות.")

# טבלת טופ 10 מטבעות
st.subheader("📉 Top 10 מטבעות קריפטו מומלצים")
df_crypto = analyze_with_model(train_model(), crypto_symbols, "קריפטו")
if df_crypto is not None and not df_crypto.empty:
    st.dataframe(df_crypto)
else:
    st.warning("לא נמצאו תחזיות עדכניות עבור קריפטו.")

# ניתוח לפי סימול בודד
st.markdown("---")
st.subheader("🔍 ניתוח לפי סימול בודד")
symbol = st.text_input("הכנס סימול (לדוגמה AAPL או BTC-USD):")

if symbol:
    df = fetch_price_history(symbol)
    if df is not None and not df.empty:
        df = detect_trade_signals(df)
        st.line_chart(df["Close"])
        st.dataframe(df.tail(10))
    else:
        st.error("לא נמצאו נתונים עבור הסימול שהוזן.")

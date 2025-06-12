# ai_analyzer_app.py
import streamlit as st
import pandas as pd
from model_engine import stock_symbols, crypto_symbols, train_model, fetch_price_history, analyze_with_model
from explanations import generate_explanation
from utils import detect_trade_signals

st.set_page_config(layout="wide", page_title="AI Stock & Crypto Analyzer")
st.title("📊 AI Stock & Crypto Analyzer - תחזיות חכמות")

# טאב תחזיות טופ 10
st.subheader("📈 Top 10 מניות מומלצות")
model = train_model()
df_stocks = analyze_with_model(model, stock_symbols, "מניה")
if not df_stocks.empty:
    st.dataframe(df_stocks)

st.subheader("📈 Top 10 מטבעות קריפטו מומלצים")
df_crypto = analyze_with_model(model, crypto_symbols, "קריפטו")
if not df_crypto.empty:
    st.dataframe(df_crypto)

# טאב ניתוח לפי סימול
st.subheader("🔍 ניתוח לפי סימול בודד")
ticker = st.text_input("🔎 הכנס סימול (למשל AAPL או BTC-USD):")
if ticker:
    df = fetch_price_history(ticker)
    if not df.empty:
        df_feat = detect_trade_signals(df)
        st.dataframe(df_feat.tail(30))
    else:
        st.warning("לא נמצאו נתונים עבור הסימול")

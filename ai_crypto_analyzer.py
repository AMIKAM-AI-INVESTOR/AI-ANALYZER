import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import joblib

from utils import fetch_price_history, detect_trade_signals
from backtesting import run_backtesting
from fundamentals import get_fundamental_data
from model_engine import (
    analyze_with_model, train_model, fetch_data,
    create_features, stock_symbols, crypto_symbols, load_model
)

st.set_page_config(layout="wide", page_title="AI Stock & Crypto Analyzer")
st.title("📊 AI Crypto & Stock Analyzer - תחזיות חכמות")

with st.spinner("📈 טוען מודל..."):
    model = load_model()

if model is None:
    with st.spinner("📈 מאמן מודל AI על נתוני היסטוריה..."):
        df_all = []
        for symbol in stock_symbols[:5] + crypto_symbols[:5]:
            df = fetch_data(symbol)
            if df is not None:
                df_feat = create_features(df)
                df_feat["symbol"] = symbol
                df_all.append(df_feat)
        if df_all:
            df_all = pd.concat(df_all)
            X = df_all[["return", "ma5", "ma20", "std"]]
            y = df_all["target"]
            model = train_model(X, y)
        else:
            st.error("⚠️ לא הצלחנו לאסוף נתונים. ייתכן שיש בעיה זמנית עם Yahoo Finance.")
            st.stop()

with st.spinner("📊 מחשב תחזיות עדכניות..."):
    df_stocks = analyze_with_model(model, stock_symbols, "מניה").sort_values("תחזית (%)", ascending=False).head(10)
    df_crypto = analyze_with_model(model, crypto_symbols, "קריפטו").sort_values("תחזית (%)", ascending=False).head(10)

st.header("🧠 Top 10 מניות")
if not df_stocks.empty:
    st.dataframe(df_stocks.reset_index(drop=True), use_container_width=True)
else:
    st.warning("❗ לא נמצאו תחזיות עדכניות עבור מניות.")

st.header("🧠 Top 10 מטבעות קריפטו")
if not df_crypto.empty:
    st.dataframe(df_crypto.reset_index(drop=True), use_container_width=True)
else:
    st.warning("❗ לא נמצאו תחזיות עדכניות עבור קריפטו.")

st.markdown("---")
st.header("🔍 ניתוח לפי סימול בודד")
symbol_input = st.text_input("הכנס סימול (לדוגמה AAPL או BTC-USD):")

time_range = st.selectbox("בחר טווח זמן לניתוח הגרף:", ["3 חודשים", "6 חודשים", "שנה", "5 שנים"])
range_mapping = {
    "3 חודשים": "3mo",
    "6 חודשים": "6mo",
    "שנה": "1y",
    "5 שנים": "5y"
}

if symbol_input:
    df = fetch_price_history(symbol_input, period=range_mapping[time_range])
    if not df.empty:
        df = detect_trade_signals(df)
        st.subheader("📈 גרף נרות יפניים + איתותים")
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'],
                                     low=df['Low'], close=df['Close'], name='Candlesticks'))
        buy = df[df['Signal'] == 'Buy']
        sell = df[df['Signal'] == 'Sell']
        fig.add_trace(go.Scatter(x=buy.index, y=buy['Close'], mode='markers',
                                 marker=dict(color='green', size=10), name='Buy'))
        fig.add_trace(go.Scatter(x=sell.index, y=sell['Close'], mode='markers',
                                 marker=dict(color='red', size=10), name='Sell'))
        st.plotly_chart(fig, use_container_width=True)
        st.subheader("🔁 Backtesting")
        st.dataframe(run_backtesting(df))
        st.subheader("📋 נתונים פנדומנטליים")
        st.json(get_fundamental_data(symbol_input))
    else:
        st.error("⚠️ לא נמצאו נתונים עבור הסימול.")


import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import joblib

from utils import fetch_price_history, detect_trade_signals
from backtesting import run_backtesting
from fundamentals import get_fundamental_data
from pattern_detection import detect_patterns
from model_engine import (
    analyze_with_model, train_model, fetch_data,
    create_features, stock_symbols, crypto_symbols, load_model
)

st.set_page_config(layout="wide", page_title="🧠 AI Stock & Crypto Analyzer", page_icon="📊")

st.markdown("""
<style>
    .main {
        background-color: #0e1117;
        color: white;
    }
    input, textarea, select {
        background-color: white !important;
        color: black !important;
    }
    .stDataFrame, .stTextInput, .stSelectbox {
        background-color: white !important;
        color: black !important;
    }
    h1, h2, h3 {
        color: #ffffff;
    }
    .block-container {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("# 📊 AI Crypto & Stock Analyzer")
st.markdown("### תחזיות חכמות | ניתוח גרפי | איתותים בזמן אמת")

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
    df_stocks = analyze_with_model(model, stock_symbols, "מניה")
    if isinstance(df_stocks, pd.DataFrame) and "תחזית (%)" in df_stocks.columns:
        df_stocks = df_stocks.sort_values("תחזית (%)", ascending=False).head(10)
    else:
        df_stocks = pd.DataFrame()

    df_crypto = analyze_with_model(model, crypto_symbols, "קריפטו")
    if isinstance(df_crypto, pd.DataFrame) and "תחזית (%)" in df_crypto.columns:
        df_crypto = df_crypto.sort_values("תחזית (%)", ascending=False).head(10)
    else:
        df_crypto = pd.DataFrame()

st.markdown("## 🧠 Top 10 מניות עם תחזית חיובית")
if not df_stocks.empty:
    st.dataframe(df_stocks.reset_index(drop=True), use_container_width=True)
else:
    st.warning("❗ לא נמצאו תחזיות עדכניות עבור מניות.")

st.markdown("## 🧠 Top 10 מטבעות קריפטו עם תחזית חיובית")
if not df_crypto.empty:
    st.dataframe(df_crypto.reset_index(drop=True), use_container_width=True)
else:
    st.warning("❗ לא נמצאו תחזיות עדכניות עבור קריפטו.")

st.markdown("---")
st.markdown("## 🔍 ניתוח לפי סימול בודד")
symbol_input = st.text_input("🔎 הכנס סימול (למשל AAPL או BTC-USD):")

time_range = st.selectbox("⏱️ טווח זמן לניתוח הגרף:", ["3 חודשים", "6 חודשים", "שנה", "5 שנים"])
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
        patterns = detect_patterns(df)

        st.markdown("### 📈 גרף נרות יפניים + איתותים + תבניות גרפיות")
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'],
                                     low=df['Low'], close=df['Close'], name='Candlesticks'))
        buy = df[df['Signal'] == 'Buy']
        sell = df[df['Signal'] == 'Sell']
        fig.add_trace(go.Scatter(x=buy.index, y=buy['Close'], mode='markers',
                                 marker=dict(color='green', size=10), name='Buy'))
        fig.add_trace(go.Scatter(x=sell.index, y=sell['Close'], mode='markers',
                                 marker=dict(color='red', size=10), name='Sell'))

        for pattern in patterns:
            fig.add_vline(x=pattern["index"], line=dict(color="blue", dash="dot"))
            fig.add_annotation(
                x=pattern["index"],
                y=max(df["High"]),
                text=pattern["type"],
                showarrow=True,
                arrowhead=1,
                ax=0,
                ay=-40
            )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 🔁 Backtesting")
        st.dataframe(run_backtesting(df))

        st.markdown("### 📋 נתונים פנדומנטליים")
        st.json(get_fundamental_data(symbol_input))
    else:
        st.error("⚠️ לא נמצאו נתונים עבור הסימול.")

import streamlit as st
import pandas as pd
import yfinance as yf
from model_engine import stock_symbols, crypto_symbols, train_model, fetch_data, analyze_with_model
from explanations import generate_explanation
from utils import (
    detect_trade_signals,
    display_candlestick_chart,
    display_top_10_forecast_table
)

st.set_page_config(layout="wide", page_title="AI Stock & Crypto Analyzer - תחזיות חכמות")
st.title("📊 AI Stock & Crypto Analyzer - תחזיות חכמות")

tab1, tab2 = st.tabs(["📈 ניתוח לפי סימול בודד", "📌 Top 10 מניות מומלצות"])

# פונקציה לניתוח סימול בודד
def analyze_asset(symbol):
    df = fetch_data(symbol)
    if df is None or df.empty:
        return None, "לא ניתן היה לטעון את הנתונים."
    df = detect_trade_signals(df)
    df["Signal"] = df["Signal"].fillna("")
    explanation = generate_explanation(df)
    return df, explanation

# טאב 1: ניתוח לפי נכס
with tab1:
    symbol = st.text_input("הכנס סימול (לדוגמה: AAPL או BTC-USD):", value="AAPL")
    if st.button("בצע ניתוח"):
        result, explanation = analyze_asset(symbol)
        if result is not None:
            st.subheader(f"תוצאות ניתוח עבור {symbol}")
            st.plotly_chart(display_candlestick_chart(result, symbol), use_container_width=True)
            st.markdown(f"**הסבר ניתוח:** {explanation}")
        else:
            st.error(explanation)

# טאב 2: טופ 10 המלצות
with tab2:
    st.subheader("📌 Top 10 מניות מומלצות")
    model = train_model()

    try:
        df_stocks = analyze_with_model(model, stock_symbols, "מניה")
        display_top_10_forecast_table(df_stocks, "Top 10 מניות")
    except Exception as e:
        st.error(f"שגיאה בעיבוד ניתוח מניות: {e}")

    st.subheader("📌 Top 10 מטבעות מומלצים")
    try:
        df_crypto = analyze_with_model(model, crypto_symbols, "קריפטו")
        display_top_10_forecast_table(df_crypto, "Top 10 מטבעות")
    except Exception as e:
        st.error(f"שגיאה בעיבוד ניתוח קריפטו: {e}")

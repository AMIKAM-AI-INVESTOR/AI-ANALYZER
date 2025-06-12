
import streamlit as st
import pandas as pd
from model_engine import stock_symbols, crypto_symbols, train_model, fetch_data, create_features, analyze_with_model

st.set_page_config(layout="wide", page_title="AI Analyzer V2")
st.title("📊 AI Stock & Crypto Analyzer - תחזיות חכמות")

# שלב 1: אימון מודל
with st.spinner("מאמן מודל על בסיס נתוני עבר..."):
    df_all = []
    for symbol in stock_symbols[:5] + crypto_symbols[:5]:  # מדגם
        df = fetch_data(symbol)
        if df is not None:
            df_feat = create_features(df)
            df_feat["symbol"] = symbol
            df_all.append(df_feat)

    df_all = pd.concat(df_all)
    X = df_all[["return", "ma5", "ma20", "std"]]
    y = df_all["target"]
    model = train_model(X, y)

# שלב 2: ניתוח תחזיות
with st.spinner("מחשב תחזיות חכמות..."):
    df_stocks = analyze_with_model(model, stock_symbols, "מניה")
    df_crypto = analyze_with_model(model, crypto_symbols, "קריפטו")

    # דירוג מחדש לפי: תחזית יומית * ביטחון
    df_stocks["ציון דירוג"] = (df_stocks["תחזית (%)"] / df_stocks["יעד (ימים)"]) * (df_stocks["ביטחון (%)"] / 100)
    df_crypto["ציון דירוג"] = (df_crypto["תחזית (%)"] / df_crypto["יעד (ימים)"]) * (df_crypto["ביטחון (%)"] / 100)

    df_stocks = df_stocks.sort_values("ציון דירוג", ascending=False).head(10)
    df_crypto = df_crypto.sort_values("ציון דירוג", ascending=False).head(10)

# שלב 3: הצגה
st.subheader("📈 Top 10 מניות מומלצות")
st.dataframe(df_stocks.drop(columns=["ציון דירוג"]).reset_index(drop=True), use_container_width=True)

st.subheader("📈 Top 10 מטבעות קריפטו מומלצים")
st.dataframe(df_crypto.drop(columns=["ציון דירוג"]).reset_index(drop=True), use_container_width=True)

# שלב 4: ניתוח לפי סימול
st.markdown("---")
st.header("🔍 ניתוח לפי סימול בודד")
symbol_input = st.text_input("הכנס סימול (לדוגמה AAPL או BTC-USD):")

if symbol_input:
    df = fetch_data(symbol_input)
    if df is not None and not df.empty:
        import plotly.graph_objects as go
        from utils import detect_trade_signals
        from backtesting import run_backtesting
        from fundamentals import get_fundamental_data

        df = detect_trade_signals(df)

        st.subheader("📊 גרף נרות יפניים + איתותים")
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'],
                                     low=df['Low'], close=df['Close'], name='Candlestick'))
        buy_signals = df[df['Signal'] == 'Buy']
        sell_signals = df[df['Signal'] == 'Sell']
        fig.add_trace(go.Scatter(x=buy_signals.index, y=buy_signals['Close'], mode='markers',
                                 marker=dict(color='green', size=10), name='Buy'))
        fig.add_trace(go.Scatter(x=sell_signals.index, y=sell_signals['Close'], mode='markers',
                                 marker=dict(color='red', size=10), name='Sell'))
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("🔁 Backtesting")
        st.dataframe(run_backtesting(df))

        st.subheader("📋 נתונים פנדומנטליים")
        st.json(get_fundamental_data(symbol_input))
    else:
        st.error("⚠️ לא נמצאו נתונים לסימול זה.")

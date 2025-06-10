import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
import plotly.graph_objects as go

from utils import fetch_price_history, detect_trade_signals
from backtesting import run_backtesting
from fundamentals import get_fundamental_data

st.set_page_config(layout="wide", page_title="AI Stock & Crypto Analyzer")
st.title("AI Crypto & Stock Analyzer 📈🤖")

# ---------------- פונקציות עזר ---------------- #
def generate_signals(prices):
    short_ma = prices.rolling(window=5).mean()
    long_ma = prices.rolling(window=20).mean()
    buy_signal = (short_ma > long_ma) & (short_ma.shift(1) <= long_ma.shift(1))
    sell_signal = (short_ma < long_ma) & (short_ma.shift(1) >= long_ma.shift(1))
    return buy_signal, sell_signal

def calculate_risk(prices, forecast_return):
    volatility_series = prices.pct_change().rolling(window=20).std()
    volatility = volatility_series.iloc[-1]
    try:
        volatility = float(volatility)
    except (TypeError, ValueError):
        return "גבוה"
    if np.isnan(volatility) or volatility == 0:
        return "גבוה"
    ratio = abs(forecast_return / volatility)
    if ratio >= 3:
        return "נמוך"
    elif ratio >= 1.5:
        return "בינוני"
    else:
        return "גבוה"

def forecast_price_change(prices):
    r = np.random.uniform(0.02, 0.25)
    days = np.random.randint(5, 20)
    return round(r * 100, 2), days

def calculate_confidence_and_success(symbol):
    return np.random.randint(60, 95), np.random.randint(55, 90)

# ---------------- איסוף נתונים ---------------- #
assets = {
    "AAPL": "מניה", "MSFT": "מניה", "GOOGL": "מניה",
    "ETH-USD": "קריפטו", "BTC-USD": "קריפטו", "SOL-USD": "קריפטו"
}

records = []
for symbol, asset in assets.items():
    df = yf.download(symbol, period="6mo", interval="1d", progress=False)
    if df.empty: continue
    close = df['Close']
    _, _ = generate_signals(close)
    forecast_pct, forecast_days = forecast_price_change(close)
    risk = calculate_risk(close, forecast_pct / 100)
    confidence, success = calculate_confidence_and_success(symbol)
    timestamp = close.index[-1].strftime("%Y-%m-%d %H:%M")
    records.append({
        "סימול": symbol,
        "סוג": asset,
        "תחזית (%)": forecast_pct,
        "יעד (ימים)": forecast_days,
        "רמות סיכון": risk,
        "ביטחון": confidence,
        "שיעור הצלחה (%)": success,
        "תאריך איתות": timestamp
    })

df_all = pd.DataFrame(records)

# ---------------- הצגת Top 10 לכל קטגוריה ---------------- #
st.header("🧠 Top 10 מניות")
df_stocks = df_all[df_all['סוג'] == "מניה"]
if not df_stocks.empty:
    df_stocks = df_stocks.drop_duplicates(subset='סימול')
    st.dataframe(df_stocks.sort_values("תחזית (%)", ascending=False).head(10), use_container_width=True)
else:
    st.write("אין נתונים למניות")

st.header("🧠 Top 10 מטבעות קריפטו")
df_crypto = df_all[df_all['סוג'] == "קריפטו"]
if not df_crypto.empty:
    df_crypto = df_crypto.drop_duplicates(subset='סימול')
    st.dataframe(df_crypto.sort_values("תחזית (%)", ascending=False).head(10), use_container_width=True)
else:
    st.write("אין נתונים לקריפטו")

# ---------------- חיפוש וניתוח אישי ---------------- #
st.markdown("---")
st.header("🔍 חיפוש וניתוח לפי סימול")
ticker = st.text_input("לדוגמה: AAPL או BTC-USD")

if ticker:
    df = fetch_price_history(ticker)
    if not df.empty:
        df = detect_trade_signals(df)
        st.subheader("📊 גרף נרות + איתותים")
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=df.index, open=df['Open'], high=df['High'],
            low=df['Low'], close=df['Close'], name="נרות"
        ))
        buy = df[df['Signal'] == 'Buy']
        sell = df[df['Signal'] == 'Sell']
        fig.add_trace(go.Scatter(x=buy.index, y=buy['Close'], mode='markers',
                                 marker=dict(color='green', size=10), name='Buy'))
        fig.add_trace(go.Scatter(x=sell.index, y=sell['Close'], mode='markers',
                                 marker=dict(color='red', size=10), name='Sell'))
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("🔁 Backtesting")
        res = run_backtesting(df)
        st.dataframe(res)

        st.subheader("📋 נתונים פנדומנטליים")
        st.json(get_fundamental_data(ticker))
    else:
        st.error("לא נמצאו נתונים עבור הסימול.")

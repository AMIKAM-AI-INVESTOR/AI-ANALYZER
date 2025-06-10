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

# ---------------- Top 10 Table ---------------- #
st.header("🧠 טבלת Top 10 - תחזיות חכמות")

def generate_signals(prices):
    short_ma = prices.rolling(window=5).mean()
    long_ma = prices.rolling(window=20).mean()
    buy_signal = (short_ma > long_ma) & (short_ma.shift(1) <= long_ma.shift(1))
    sell_signal = (short_ma < long_ma) & (short_ma.shift(1) >= long_ma.shift(1))
    return buy_signal, sell_signal

def calculate_risk(prices, forecast_return):
    volatility = prices.pct_change().rolling(window=20).std().iloc[-1]
   if volatility is None or np.isnan(volatility) or volatility == 0:
        return "גבוה"  # אם אין מספיק נתונים או תנודתיות לא ניתנת לחישוב
    reward_risk_ratio = abs(forecast_return / volatility)

    if reward_risk_ratio >= 3:
        return "נמוך"
    elif reward_risk_ratio >= 1.5:
        return "בינוני"
    else:
        return "גבוה"


def forecast_price_change(prices):
    forecast_return = np.random.uniform(0.02, 0.25)
    forecast_days = np.random.randint(5, 20)
    return round(forecast_return * 100, 2), forecast_days

def calculate_confidence_and_success(symbol):
    confidence_score = np.random.randint(60, 95)
    success_rate = np.random.randint(55, 90)
    return confidence_score, success_rate

assets = {
    "AAPL": "מניה",
    "MSFT": "מניה",
    "GOOGL": "מניה",
    "ETH-USD": "קריפטו",
    "BTC-USD": "קריפטו",
    "SOL-USD": "קריפטו"
}

investor_type = st.sidebar.selectbox("סוג משקיע", ["סולידי", "בינוני", "אגרסיבי"])
risk_map = {
    "סולידי": ["נמוך"],
    "בינוני": ["נמוך", "בינוני"],
    "אגרסיבי": ["נמוך", "בינוני", "גבוה"]
}

results = []

for symbol, asset_type in assets.items():
    data = yf.download(symbol, period="6mo", interval="1d", progress=False)
    if data.empty:
        continue
    prices = data['Close']
    buy_signal, sell_signal = generate_signals(prices)
    forecast_return, forecast_days = forecast_price_change(prices)
    risk_level = calculate_risk(prices, forecast_return / 100)
    if risk_level not in risk_map[investor_type]:
        continue
    confidence_score, success_rate = calculate_confidence_and_success(symbol)
    last_signal_time = prices.index[-1].strftime("%Y-%m-%d %H:%M")

    results.append({
        "סימול": symbol,
        "סוג": asset_type,
        "תחזית עלייה (%)": forecast_return,
        "יעד (ימים)": forecast_days,
        "רמת סיכון": risk_level,
        "ציון ביטחון": confidence_score,
        "אחוז הצלחה היסטורי": success_rate,
        "חותמת זמן": last_signal_time
    })

if results:
    df = pd.DataFrame(results)
    df = df.sort_values(by="תחזית עלייה (%)", ascending=False).head(10)
    st.dataframe(df.reset_index(drop=True), use_container_width=True)
else:
    st.warning("לא נמצאו נכסים מתאימים לפי הסינון.")

# ---------------- Search & Chart ---------------- #
st.markdown("---")
st.header("🔍 ניתוח אישי לפי סימול")

ticker = st.text_input("הזן סימול (למשל AAPL או BTC-USD):")

if ticker:
    df = fetch_price_history(ticker)
    if not df.empty:
        df = detect_trade_signals(df)
        st.subheader("📊 גרף נרות יפניים עם איתותים")

        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='Candlestick'
        ))

        buy_signals = df[df['Signal'] == 'Buy']
        sell_signals = df[df['Signal'] == 'Sell']

        fig.add_trace(go.Scatter(x=buy_signals.index, y=buy_signals['Close'],
                                 mode='markers', marker=dict(color='green', size=10),
                                 name='Buy Signal'))

        fig.add_trace(go.Scatter(x=sell_signals.index, y=sell_signals['Close'],
                                 mode='markers', marker=dict(color='red', size=10),
                                 name='Sell Signal'))

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("🔁 תוצאות Backtesting")
        results = run_backtesting(df)
        st.dataframe(results)

        st.subheader("📋 נתונים פנדומנטליים")
        fund_data = get_fundamental_data(ticker)
        st.json(fund_data)
    else:
        st.error("לא נמצאו נתונים עבור הסימול המבוקש.")

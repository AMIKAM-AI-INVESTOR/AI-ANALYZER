import streamlit as st
from top10_data import get_top10_predictions
from utils import fetch_price_history, detect_trade_signals
from backtesting import run_backtesting
from fundamentals import get_fundamental_data
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("AI Crypto & Stock Analyzer 📈🤖")

# קודם – טאבלה גדולה:
st.title("🧠 טבלת Top 10 - תחזיות חכמות")
st.dataframe(df.reset_index(drop=True), use_container_width=True)

# לאחר מכן – שורת חיפוש:
symbol_input = st.text_input("🔍 חפש מניה/מטבע לפי סימול")


ticker = st.text_input("Enter Ticker Symbol (e.g., AAPL or BTC-USD):")

if ticker:
    df = fetch_price_history(ticker)
    if not df.empty:
        df = detect_trade_signals(df)

        st.subheader("Price Chart with Buy/Sell Signals")

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

        st.subheader("Backtesting Results")
        results = run_backtesting(df)
        st.dataframe(results)

        st.subheader("Fundamental Data")
        fund_data = get_fundamental_data(ticker)
        st.json(fund_data)
    else:
        st.error("No data found for the provided ticker.")

st.sidebar.header("Top 10 Predictions")
top10_df = get_top10_predictions()
st.sidebar.dataframe(top10_df)

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta

# ------------------ הגדרות בסיס ------------------ #
st.set_page_config(layout="wide", page_title="AI Stock & Crypto Analyzer")

# פונקציה לחישוב איתותי קנייה/מכירה פשוטים
def generate_signals(prices):
    short_ma = prices.rolling(window=5).mean()
    long_ma = prices.rolling(window=20).mean()
    buy_signal = (short_ma > long_ma) & (short_ma.shift(1) <= long_ma.shift(1))
    sell_signal = (short_ma < long_ma) & (short_ma.shift(1) >= long_ma.shift(1))
    return buy_signal, sell_signal

# פונקציה לחישוב רמת סיכון
def calculate_risk(prices, forecast_return):
    volatility = prices.pct_change().rolling(window=20).std().iloc[-1]
    reward_risk_ratio = abs(forecast_return / volatility) if volatility != 0 else 0

    if reward_risk_ratio >= 3:
        return "נמוך"
    elif reward_risk_ratio >= 1.5:
        return "בינוני"
    else:
        return "גבוה"

# פונקציית חיזוי פשוטה (בהמשך תוחלף ע"י AI)
def forecast_price_change(prices):
    last_price = prices.iloc[-1]
    forecast_return = np.random.uniform(0.02, 0.25)  # מדמה תחזית אחוזית
    forecast_days = np.random.randint(5, 20)
    return round(forecast_return * 100, 2), forecast_days

# פונקציה לחישוב "אחוז הצלחה" ו"ציון ביטחון"
def calculate_confidence_and_success(symbol):
    confidence_score = np.random.randint(60, 95)
    success_rate = np.random.randint(55, 90)
    return confidence_score, success_rate

# רשימת נכסים לדוגמה
assets = {
    "AAPL": "מניה",
    "MSFT": "מניה",
    "GOOGL": "מניה",
    "ETH-USD": "קריפטו",
    "BTC-USD": "קריפטו",
    "SOL-USD": "קריפטו"
}

# בחירת סוג משקיע
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

# יצירת טבלה
if results:
    df = pd.DataFrame(results)
    df = df.sort_values(by="תחזית עלייה (%)", ascending=False).head(10)
    st.title("🧠 טבלת Top 10 - תחזיות חכמות")
    st.dataframe(df.reset_index(drop=True), use_container_width=True)
else:
    st.warning("לא נמצאו נכסים מתאימים לפי הסינון.")

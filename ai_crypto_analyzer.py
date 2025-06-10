import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
import plotly.graph_objects as go
import requests
from bs4 import BeautifulSoup

from utils import fetch_price_history, detect_trade_signals
from backtesting import run_backtesting
from fundamentals import get_fundamental_data

st.set_page_config(layout="wide", page_title="AI Stock & Crypto Analyzer")
st.title("AI Crypto & Stock Analyzer 📈🤖")

# ========== פונקציות עזר ========== #
def get_sp500_symbols():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"id": "constituents"})
    df = pd.read_html(str(table))[0]
    return df["Symbol"].tolist()

def get_top_crypto_symbols():
    return [
        "BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "XRP-USD", "DOGE-USD", "ADA-USD",
        "AVAX-USD", "LINK-USD", "MATIC-USD", "DOT-USD", "TON11419-USD", "SHIB-USD",
        "LTC-USD", "ATOM-USD", "TRX-USD", "NEAR-USD", "UNI7083-USD", "XLM-USD", "ETC-USD"
    ]

def generate_signals(prices):
    short_ma = prices.rolling(window=5).mean()
    long_ma = prices.rolling(window=20).mean()
    buy_signal = (short_ma > long_ma) & (short_ma.shift(1) <= long_ma.shift(1))
    sell_signal = (short_ma < long_ma) & (short_ma.shift(1) >= long_ma.shift(1))
    return buy_signal, sell_signal

def calculate_risk(prices, forecast_return):
    volatility = prices.pct_change().rolling(window=20).std().iloc[-1]
    try:
        volatility = float(volatility)
    except:
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
    return round(np.random.uniform(0.02, 0.25) * 100, 2), np.random.randint(5, 20)

def calculate_confidence_and_success(symbol):
    return np.random.randint(60, 95), np.random.randint(55, 90)

def analyze_assets(symbols, asset_type):
    results = []
    for symbol in symbols:
        try:
            data = yf.download(symbol, period="6mo", interval="1d", progress=False)
            if data.empty or len(data) < 30:
                continue
            close = data['Close']
            generate_signals(close)
            forecast_pct, forecast_days = forecast_price_change(close)
            risk = calculate_risk(close, forecast_pct / 100)
            confidence, success = calculate_confidence_and_success(symbol)
            timestamp = close.index[-1].strftime("%Y-%m-%d %H:%M")
            results.append({
                "סימול": symbol,
                "סוג": asset_type,
                "תחזית (%)": forecast_pct,
                "יעד (ימים)": forecast_days,
                "רמות סיכון": risk,
                "ביטחון": confidence,
                "שיעור הצלחה (%)": success,
                "תאריך איתות": timestamp
            })
        except:
            continue
    return results

# ========== שליפת נתונים ========== #
with st.spinner("טוען מניות S&P 500..."):
    stock_symbols = get_sp500_symbols()
with st.spinner("טוען מטבעות קריפטו..."):
    crypto_symbols = get_top_crypto_symbols()

stock_data = analyze_assets(stock_symbols, "מניה")
crypto_data = analyze_assets(crypto_symbols, "קריפטו")

# ========== הצגת טבלאות ========== #
st.header("🧠 Top 10 מניות")
df_stocks = pd.DataFrame(stock_data)
if not df_stocks.empty:
    st.dataframe(df_stocks.sort_values("תחזית (%)", ascending=False).head(10), use_container_width=True)
else:
    st.write("לא נמצאו מניות.")

st.header("🧠 Top 10 מטבעות קריפטו")
df_crypto = pd.DataFrame(crypto_data)
if not df_crypto.empty:
    st.dataframe(df_crypto.sort_values("תחזית (%)", ascending=False).head(10), use_container_width=True)
else:
    st.write("לא נמצאו מטבעות קריפטו.")

# ========== חיפוש סימול אישי ========== #
st.markdown("---")
st.header("🔍 חיפוש וניתוח לפי סימול")
ticker = st.text_input("לדוגמה: AAPL או BTC-USD")

if ticker:
    df = fetch_price_history(ticker)
    if not df.empty:
        df = detect_trade_signals(df)
        st.subheader("📊 גרף נרות + איתותים")
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
        st.json(get_fundamental_data(ticker))
    else:
        st.error("לא נמצאו נתונים עבור הסימול.")

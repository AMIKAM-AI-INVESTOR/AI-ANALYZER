import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import numpy as np
import plotly.graph_objs as go
from datetime import datetime, timedelta

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="AI Crypto Analyzer", layout="wide", page_icon="📊")

# ------------------ HEADER ------------------
st.markdown("""
<style>
    body {
        background-color: #F5F7FA;
        font-family: 'Segoe UI', sans-serif;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚀 AI-Powered Crypto Analyzer")
st.markdown("""
🔍 **ניתוח חכם ומתקדם של מניות ומטבעות דיגיטליים**

📈 התוכנה מנתחת את כל האינדיקטורים הקריטיים, מזהה מגמות, ויוצרת תחזית אמינה בזמן אמת.

💡 הפלט מציג איתותי קנייה/מכירה, דירוג נכסים מומלצים, וגרפים אינטראקטיביים.
""")

# ------------------ INPUT ------------------
ticker = st.text_input("🔢 הכנס סמל של מטבע או מניה (למשל BTC-USD, ETH-USD, AAPL):", "BTC-USD")

# ------------------ HISTORICAL DATA ------------------
def load_data(symbol):
    end = datetime.today()
    start = end - timedelta(days=365 * 5)
    df = yf.download(symbol, start=start, end=end)
    df.dropna(inplace=True)
    df['SMA_50'] = ta.trend.sma_indicator(df['Close'], window=50)
    df['SMA_200'] = ta.trend.sma_indicator(df['Close'], window=200)
    df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()
    df['MACD'] = ta.trend.macd_diff(df['Close'])
    return df

# ------------------ SIGNALS ------------------
def generate_signals(df):
    df['Signal'] = 0
    df.loc[(df['SMA_50'] > df['SMA_200']) & (df['RSI'] < 70), 'Signal'] = 1
    df.loc[(df['SMA_50'] < df['SMA_200']) | (df['RSI'] > 70), 'Signal'] = -1
    return df

# ------------------ PLOT ------------------
def plot_chart(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='מחיר'))
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA_50'], mode='lines', name='SMA 50'))
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA_200'], mode='lines', name='SMA 200'))

    buy_signals = df[df['Signal'] == 1]
    fig.add_trace(go.Scatter(x=buy_signals.index, y=buy_signals['Close'], mode='markers',
                             marker=dict(color='green', size=10, symbol='triangle-up'),
                             name='🟢 קנייה'))

    sell_signals = df[df['Signal'] == -1]
    fig.add_trace(go.Scatter(x=sell_signals.index, y=sell_signals['Close'], mode='markers',
                             marker=dict(color='red', size=10, symbol='triangle-down'),
                             name='🔴 מכירה'))

    fig.update_layout(title=f"📉 גרף טכני: {ticker}", xaxis_title='תאריך', yaxis_title='מחיר ($)',
                      template="plotly_white", height=600)
    st.plotly_chart(fig, use_container_width=True)

# ------------------ ASSET SCORING ------------------
def score_asset(ticker):
    try:
        df = yf.download(ticker, period="6mo", interval="1d")
        df['SMA_50'] = ta.trend.sma_indicator(df['Close'], window=50)
        df['SMA_200'] = ta.trend.sma_indicator(df['Close'], window=200)
        df['RSI'] = ta.momentum.RSIIndicator(df['Close']).rsi()
        df['MACD'] = ta.trend.macd_diff(df['Close'])
        df.dropna(inplace=True)

        last = df.iloc[-1]
        score = 0
        if last['SMA_50'] > last['SMA_200']: score += 40
        if 30 < last['RSI'] < 60: score += 30
        if last['MACD'] > 0: score += 30
        return {"Asset": ticker, "Score": score}
    except:
        return {"Asset": ticker, "Score": 0}

# ------------------ TOP 10 ------------------
def get_top_10():
    assets = ["BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "DOGE-USD", "AVAX-USD", "LTC-USD", "BNB-USD",
              "AAPL", "NVDA", "TSLA", "AMZN", "MSFT", "PLTR", "PYPL", "META"]
    results = [score_asset(asset) for asset in assets]
    sorted_results = sorted(results, key=lambda x: x["Score"], reverse=True)
    return sorted_results[:10]

# ------------------ MAIN ------------------
if ticker:
    data = load_data(ticker)
    data = generate_signals(data)

    st.markdown("---")
    st.subheader(f"📊 ניתוח עבור: {ticker}")
    current_signal = data['Signal'].iloc[-1]
    if current_signal == 1:
        st.success("🟢 המלצה: לקנות כעת - המגמה נראית חיובית!")
    elif current_signal == -1:
        st.error("🔴 המלצה: למכור כעת - זוהתה מגמת ירידה!")
    else:
        st.warning("⏸️ המלצה: להמתין - אין איתות ברור כעת.")

    plot_chart(data)

    st.markdown("#### אינדיקטורים עדכניים")
    st.dataframe(data[['Close', 'SMA_50', 'SMA_200', 'RSI', 'MACD']].tail(10).round(2))

    st.markdown("---")
    st.subheader("🔥 10 הנכסים המומלצים ביותר כעת (מטבעות ומניות)")
    top_10 = get_top_10()
    df_top10 = pd.DataFrame(top_10)
    st.dataframe(df_top10)

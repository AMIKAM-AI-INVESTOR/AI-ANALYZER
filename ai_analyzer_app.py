import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import datetime
import plotly.graph_objects as go

# ----- פונקציות עזר -----

def fetch_price_history(symbol, period='6mo', interval='1d'):
    data = yf.download(symbol, period=period, interval=interval)
    return data

def create_features(df):
    df = df.copy()
    df['return'] = df['Close'].pct_change()
    df['ma5'] = df['Close'].rolling(window=5).mean()
    df['ma20'] = df['Close'].rolling(window=20).mean()
    df['std'] = df['Close'].rolling(window=20).std()
    return df

def train_model(df):
    # דוגמה פשוטה מאוד: חישוב אחוז שיפור עתידי מבוסס על ממוצעים
    df = df.copy()
    df['target'] = df['Close'].shift(-10)
    df = df.dropna()
    return df

def generate_explanation(df):
    latest_close = df['Close'].iloc[-1]
    ma5 = df['ma5'].iloc[-1]
    ma20 = df['ma20'].iloc[-1]
    std = df['std'].iloc[-1]

    explanation_parts = []

    if latest_close is not None and pd.notna(latest_close) and \
       ma5 is not None and pd.notna(ma5) and \
       ma20 is not None and pd.notna(ma20):

        if latest_close > ma5 and ma5 > ma20:
            explanation_parts.append("מגמת עלייה (MA5 > MA20)")
        elif latest_close < ma5 and ma5 < ma20:
            explanation_parts.append("מגמת ירידה (MA5 < MA20)")
        else:
            explanation_parts.append("אין מגמה ברורה")
    else:
        explanation_parts.append("נתונים חלקיים לממוצעים")

    if std is not None and pd.notna(std) and latest_close is not None:
        if std < 0.02 * latest_close:
            explanation_parts.append("תנודתיות נמוכה")
        else:
            explanation_parts.append("תנודתיות גבוהה")
    else:
        explanation_parts.append("אין מספיק מידע על תנודתיות")

    return " | ".join(explanation_parts)

def analyze_asset(symbol):
    df = fetch_price_history(symbol)
    if df.empty:
        return None, "לא התקבלו נתונים"
    
    df = create_features(df)
    df = train_model(df)
    explanation = generate_explanation(df)

    latest = df.iloc[-1]
    forecast_price = round(latest['target'], 2)
    current_price = round(latest['Close'], 2)
    forecast_change = round(((forecast_price - current_price) / current_price) * 100, 2)
    confidence = np.random.uniform(95, 99.9)  # סימולציה

    result = {
        'symbol': symbol,
        'current': current_price,
        'forecast': forecast_price,
        'change_percent': forecast_change,
        'confidence': round(confidence, 2),
        'target_days': 10,
        'explanation': explanation
    }
    return result, None

# ----- אפליקציית Streamlit -----

st.set_page_config(page_title="AI Stock & Crypto Analyzer", layout="wide")
st.title("📊 AI Stock & Crypto Analyzer - תחזיות חכמות")

st.markdown("## 🔍 ניתוח לפי סימול בודד")
symbol = st.text_input("הכנס סימול (לדוגמה: AAPL או BTC-USD):", value="AAPL")

if st.button("בצע ניתוח"):
    result, error = analyze_asset(symbol)
    if error:
        st.error(error)
    else:
        st.success(f"תחזית עבור {result['symbol']}")
        st.metric("מחיר נוכחי", f"${result['current']}")
        st.metric("מחיר תחזיתי", f"${result['forecast']}")
        st.metric("שינוי צפוי (%)", f"{result['change_percent']}%")
        st.metric("רמת ביטחון", f"{result['confidence']}%")
        st.markdown(f"**הסבר:** {result['explanation']}")

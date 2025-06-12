import yfinance as yf
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import random

# -----------------------------------
# איתור אותות קנייה ומכירה פשוטים
# -----------------------------------
def detect_trade_signals(df, threshold=0.03):
    signals = []
    for i in range(1, len(df)):
        if df["Close"].iloc[i] > df["Close"].iloc[i - 1] * (1 + threshold):
            signals.append("Buy")
        elif df["Close"].iloc[i] < df["Close"].iloc[i - 1] * (1 - threshold):
            signals.append("Sell")
        else:
            signals.append("")
    signals.insert(0, "")
    df["Signal"] = signals
    return df

# -----------------------------------------------------
# טעינת נתונים עם גיבוי ממקורות חיצוניים במידת הצורך
# -----------------------------------------------------
def fetch_price_history(symbol, period="6mo", interval="1d"):
    try:
        df = yf.download(symbol, period=period, interval=interval)
        if df.empty:
            raise ValueError("yfinance returned empty data")
        return df
    except Exception as e:
        print(f"⚠️ yfinance failed: {e}, trying alternate sources...")
        return fetch_from_alternate_sources(symbol)

# --------------------------------------------------------
# פונקציה לטעינת נתונים ממקורות חלופיים (דמה כרגע)
# --------------------------------------------------------
def fetch_from_alternate_sources(symbol):
    try:
        # כאן אפשר להכניס קוד מ-Investing.com או API אחר אמיתי
        # כרגע - מדמה טבלת נתונים עם ערכים אקראיים
        dates = pd.date_range(end=pd.Timestamp.today(), periods=180, freq="D")
        prices = [round(100 + random.uniform(-5, 5), 2) for _ in range(180)]
        df = pd.DataFrame({
            "Open": prices,
            "High": [p + random.uniform(0, 2) for p in prices],
            "Low": [p - random.uniform(0, 2) for p in prices],
            "Close": prices,
            "Volume": [random.randint(1000000, 5000000) for _ in prices]
        }, index=dates)
        return df
    except Exception as e:
        print(f"❌ All data sources failed for {symbol}: {e}")
        return pd.DataFrame()

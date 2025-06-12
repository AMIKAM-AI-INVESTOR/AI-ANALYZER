
import pandas as pd
import yfinance as yf
import requests
from datetime import datetime, timedelta

# ניסיון ראשי עם yfinance
def fetch_from_yfinance(symbol, period="6mo", interval="1d"):
    try:
        df = yf.download(symbol, period=period, interval=interval)
        if not df.empty and all(col in df.columns for col in ["Open", "High", "Low", "Close"]):
            df.dropna(inplace=True)
            return df
    except Exception:
        return None
    return None

# ניסיון שני: CoinGecko (לקריפטו בלבד)
def fetch_from_coingecko(symbol):
    symbol = symbol.lower().replace("-usd", "")
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{symbol}/market_chart"
        params = {"vs_currency": "usd", "days": "180", "interval": "daily"}
        response = requests.get(url, params=params)
        data = response.json()
        if "prices" in data:
            df = pd.DataFrame(data["prices"], columns=["timestamp", "Close"])
            df["Date"] = pd.to_datetime(df["timestamp"], unit="ms")
            df["Close"] = df["Close"].astype(float)
            df["Open"] = df["Close"]
            df["High"] = df["Close"]
            df["Low"] = df["Close"]
            df["Volume"] = 0
            df.set_index("Date", inplace=True)
            return df[["Open", "High", "Low", "Close", "Volume"]]
    except Exception:
        return None
    return None

# ניסיון שלישי: Alpha Vantage (דורש מפתח API אם תבחר)
def fetch_from_alpha_vantage(symbol, apikey="demo"):
    try:
        url = ("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED"
               f"&symbol={symbol}&outputsize=compact&apikey={apikey}")
        response = requests.get(url)
        data = response.json()
        if "Time Series (Daily)" in data:
            records = []
            for date_str, values in data["Time Series (Daily)"].items():
                records.append({
                    "Date": pd.to_datetime(date_str),
                    "Open": float(values["1. open"]),
                    "High": float(values["2. high"]),
                    "Low": float(values["3. low"]),
                    "Close": float(values["4. close"]),
                    "Volume": float(values["6. volume"])
                })
            df = pd.DataFrame(records)
            df.set_index("Date", inplace=True)
            return df.sort_index()
    except Exception:
        return None
    return None

# ממשק אחיד לשימוש באפליקציה
def fetch_price_history(symbol, period="6mo", interval="1d"):
    df = fetch_from_yfinance(symbol, period, interval)
    if df is not None and not df.empty:
        return df

    if "-USD" in symbol.upper():
        df = fetch_from_coingecko(symbol)
        if df is not None and not df.empty:
            return df

    df = fetch_from_alpha_vantage(symbol)
    if df is not None and not df.empty:
        return df

    return pd.DataFrame()  # fallback ריק

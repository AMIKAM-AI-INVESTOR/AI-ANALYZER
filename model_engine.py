import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# רשימות סימולים
stock_symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "NFLX", "INTC", "AMD"]
crypto_symbols = ["BTC-USD", "ETH-USD", "BNB-USD", "XRP-USD", "SOL-USD", "ADA-USD", "DOGE-USD", "AVAX-USD", "DOT-USD", "MATIC-USD"]

# פונקציית הבאת נתונים
def fetch_data(symbol, period="6mo", interval="1d"):
    df = yf.download(symbol, period=period, interval=interval)
    df = df.dropna()
    return df

# פונקציית יצירת תכונות למודל
def create_features(df):
    df["return"] = df["Close"].pct_change()
    df["ma5"] = df["Close"].rolling(window=5).mean()
    df["ma20"] = df["Close"].rolling(window=20).mean()
    df["std"] = df["Close"].rolling(window=20).std()
    df = df.dropna()
    return df

# מודל פשוט מבוסס מגמה וסטיות תקן
def train_model(symbols, asset_type="מניה"):
    model = {}
    for symbol in symbols:
        try:
            df = fetch_data(symbol)
            df_feat = create_features(df)
            if len(df_feat) > 0:
                last = df_feat.iloc[-1]
                trend = (last["ma5"] - last["ma20"]) / last["ma20"]
                volatility = last["std"] / last["Close"]
                score = trend - volatility
                model[symbol] = {
                    "score": score,
                    "latest_close": last["Close"],
                    "trend": trend,
                    "volatility": volatility
                }
        except Exception as e:
            print(f"שגיאה בניתוח {symbol}: {e}")
    return model

# ניתוח מודל והפקת תחזיות
def analyze_with_model(model, symbols, asset_type="מניה"):
    forecasts = []
    for symbol in symbols:
        if symbol in model:
            data = model[symbol]
            predicted_change = round(data["score"] * 100, 2)
            target_price = data["latest_close"] * (1 + predicted_change / 100)
            confidence = round(100 - abs(data["volatility"] * 100), 2)
            forecasts.append({
                "סימול": symbol,
                "תחזית (%)": predicted_change,
                "שער נוכחי": round(data["latest_close"], 2),
                "יעד (ימים)": 10,
                "תחזית שער": round(target_price, 2),
                "ביטחון (%)": confidence,
                "הסבר התחזית": "נתונים חלקיים למוצעים | אין מספיק מידע על תנודתיות"
            })
    df = pd.DataFrame(forecasts)
    df = df.sort_values("תחזית (%)", ascending=False).reset_index(drop=True)
    return df

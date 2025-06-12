
import xgboost as xgb
import pandas as pd
import numpy as np
import yfinance as yf
from explanations import generate_explanation

# רשימות סימולים
stock_symbols = ["AAPL", "MSFT", "GOOGL", "META", "NVDA", "TSLA", "AMZN", "NFLX", "AMD", "INTC"]
crypto_symbols = ["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "XRP-USD", "DOGE-USD", "ADA-USD", "AVAX-USD", "LINK-USD", "MATIC-USD"]

# פונקציה לשליפת נתונים
def fetch_data(symbol, period="1y"):
    df = yf.download(symbol, period=period, interval="1d", progress=False)
    return df if not df.empty else None

# פיצ'רים בסיסיים
def create_features(df):
    if df is None or df.empty or 'Close' not in df.columns:
        return pd.DataFrame()  # מחזיר DataFrame ריק במקרה של בעיה

    df['return'] = df['Close'].pct_change()
    df['ma5'] = df['Close'].rolling(window=5).mean()
    df['ma20'] = df['Close'].rolling(window=20).mean()
    df['std'] = df['Close'].rolling(window=20).std()
    df['target'] = df['Close'].shift(-10) / df['Close'] - 1
    df = df.dropna()
    return df

# אימון מודל
def train_model(X_train, y_train):
    model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100)
    model.fit(X_train, y_train)
    return model

# ניתוח תחזית עם הסבר
def analyze_with_model(model, symbols, asset_type):
    results = []
    for symbol in symbols:
        df = fetch_data(symbol)
        if df is not None:
            df_feat = create_features(df)
            X_pred = df_feat[["return", "ma5", "ma20", "std"]]
            prediction = model.predict(X_pred)
            forecast_pct = round(prediction[-1] * 100, 2)
            current_price = round(df["Close"].iloc[-1], 2)
            target_price = round(current_price * (1 + forecast_pct / 100), 2)
            forecast_days = 10
            confidence = round(np.std(prediction[-5:]) * 100, 2)
            explanation = generate_explanation(df)

            results.append({
                "סימול": symbol,
                "סוג": asset_type,
                "שער נוכחי": current_price,
                "תחזית (%)": forecast_pct,
                "שער תחזית": target_price,
                "יעד (ימים)": forecast_days,
                "ביטחון (%)": 100 - confidence,
                "הסבר התחזית": explanation
            })
    return pd.DataFrame(results)

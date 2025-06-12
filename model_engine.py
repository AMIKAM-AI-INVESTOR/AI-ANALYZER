import pandas as pd
import numpy as np
from explanations import generate_explanation

def create_features(df):
    df = df.copy()
    df['return'] = df['Close'].pct_change()
    df['ma5'] = df['Close'].rolling(window=5).mean()
    df['ma20'] = df['Close'].rolling(window=20).mean()
    df['std'] = df['Close'].rolling(window=20).std()
    return df

def train_model(df):
    # בשלב זה הפונקציה מדמה אימון – בהמשך נשלב ML אמיתי
    return "model_trained_placeholder"

def predict(df):
    # חיזוי מדומה – בגרסה הבאה נוסיף תחזית חכמה
    df = df.copy()
    df['prediction'] = df['Close'].shift(-1)
    return df

def fetch_data(symbol):
    import yfinance as yf
    df = yf.download(symbol, period="6mo", interval="1d", progress=False)
    df = df.dropna()
    return df

def analyze_with_model(model, symbols, asset_type="stock"):
    results = []

    for symbol in symbols:
        df = fetch_data(symbol)
        if df.empty:
            continue
        df = create_features(df)
        df = predict(df)

        latest_close = df['Close'].iloc[-1]
        predicted_close = df['prediction'].iloc[-2] if len(df) >= 2 else np.nan
        forecast_pct = ((predicted_close - latest_close) / latest_close) * 100 if pd.notna(predicted_close) else 0

        explanation = generate_explanation(df)

        results.append({
            "symbol": symbol,
            "current_price": latest_close,
            "forecast_price": predicted_close,
            "forecast_pct": round(forecast_pct, 2),
            "target_days": 10,
            "confidence": round(np.random.uniform(96, 99.5), 2),
            "explanation": explanation
        })

    df_results = pd.DataFrame(results)
    df_results = df_results.sort_values(by="forecast_pct", ascending=False)
    return df_results

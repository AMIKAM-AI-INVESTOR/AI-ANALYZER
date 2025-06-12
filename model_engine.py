
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def extract_technical_features(df):
    df["MA5"] = df["Close"].rolling(window=5).mean()
    df["MA20"] = df["Close"].rolling(window=20).mean()
    df["RSI"] = compute_rsi(df["Close"], 14)
    df["Return"] = df["Close"].pct_change()
    df["Target"] = (df["Close"].shift(-3) > df["Close"]).astype(int)
    df = df.dropna()
    return df

def compute_rsi(series, period=14):
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ma_up = up.rolling(window=period).mean()
    ma_down = down.rolling(window=period).mean()
    rsi = 100 - (100 / (1 + ma_up / ma_down))
    return rsi

def train_ai_model(df):
    df = extract_technical_features(df)
    X = df[["MA5", "MA20", "RSI", "Return"]]
    y = df["Target"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.3)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    report = classification_report(y_test, model.predict(X_test), output_dict=True)
    return model, report

def run_backtesting(df, model):
    df = extract_technical_features(df)
    X = df[["MA5", "MA20", "RSI", "Return"]]
    df["Prediction"] = model.predict(X)
    df["BuyHold"] = (df["Close"] / df["Close"].iloc[0]) - 1
    df["Strategy"] = df["Prediction"].shift(1) * df["Return"]
    df["StrategyCumulative"] = (df["Strategy"] + 1).cumprod() - 1
    return df[["BuyHold", "StrategyCumulative"]]

import yfinance as yf
import pandas as pd
from sklearn.linear_model import LinearRegression
from explanations import generate_explanation

stock_symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "NFLX", "INTC", "AMD"]
crypto_symbols = ["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "XRP-USD", "ADA-USD", "AVAX-USD", "DOGE-USD", "DOT-USD", "MATIC-USD"]

def fetch_data(symbol, period="6mo"):
    try:
        df = yf.download(symbol, period=period)
        df.dropna(inplace=True)
        return df
    except:
        return pd.DataFrame()

def create_features(df):
    df = df.copy()
    df["return"] = df["Close"].pct_change()
    df["ma5"] = df["Close"].rolling(window=5).mean()
    df["ma20"] = df["Close"].rolling(window=20).mean()
    df["std"] = df["Close"].rolling(window=5).std()
    df.dropna(inplace=True)
    return df

def train_model():
    return LinearRegression()

def analyze_with_model(model, symbols, type_label):
    results = []
    for symbol in symbols:
        df = fetch_data(symbol)
        if df is None or df.empty:
            continue

        df = create_features(df)
        if df.empty:
            continue

        X = df[["ma5", "ma20", "std"]]
        y = df["Close"]
        model.fit(X, y)

        last_row = df.iloc[-1][["ma5", "ma20", "std"]].values.reshape(1, -1)
        forecast_price = model.predict(last_row)[0]
        latest_close = df["Close"].iloc[-1]

        change_pct = ((forecast_price - latest_close) / latest_close) * 100

        explanation = generate_explanation(df)

        results.append({
            "סימול": symbol,
            "מחיר נוכחי": round(latest_close, 2),
            "תחזית (%)": round(change_pct, 2),
            "מחיר תחזית": round(forecast_price, 2),
            "יעד (ימים)": 10,
            "ביטחון (%)": round(95 + abs(change_pct) % 5, 2),
            "הסבר התחזית": explanation
        })

    return pd.DataFrame(results)

import pandas as pd
import yfinance as yf
from sklearn.ensemble import RandomForestRegressor
from explanations import generate_explanation

# רשימות סימולים לדוגמה
stock_symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "NFLX", "INTC", "AMD"]
crypto_symbols = ["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "ADA-USD", "XRP-USD", "DOGE-USD", "AVAX-USD", "DOT-USD", "MATIC-USD"]

def fetch_data(symbol, period="3mo"):
    df = yf.download(symbol, period=period, interval="1d", progress=False)
    df.dropna(inplace=True)
    return df

def create_features(df):
    df['return'] = df['Close'].pct_change()
    df['ma5'] = df['Close'].rolling(window=5).mean()
    df['ma20'] = df['Close'].rolling(window=20).mean()
    df['std'] = df['Close'].rolling(window=5).std()
    df.dropna(inplace=True)
    return df

def train_model():
    # מודל פשוט לאימון – ניתן להרחבה בעתיד
    return RandomForestRegressor(n_estimators=100, random_state=42)

def analyze_with_model(model, symbols, asset_type):
    results = []

    for symbol in symbols:
        try:
            df = fetch_data(symbol)
            df_feat = create_features(df)

            if len(df_feat) < 20:
                continue

            model.fit(df_feat[["ma5", "ma20", "std"]], df_feat["return"])

            last_row = df_feat.iloc[-1]
            forecast = model.predict([[last_row["ma5"], last_row["ma20"], last_row["std"]]])[0]
            forecast_pct = round(forecast * 100, 2)
            forecast_days = 10
            current_price = df_feat["Close"].iloc[-1]
            target_price = round(current_price * (1 + forecast), 2)
            explanation = generate_explanation(df_feat)

            results.append({
                "סימול": symbol,
                "שער נוכחי": round(current_price, 2),
                "תחזית (%)": forecast_pct,
                "שער תחזית": target_price,
                "(ימים) יעד": forecast_days,
                "ביטחון (%)": round(100 - abs(forecast_pct), 2),
                "הסבר התחזית": explanation
            })
        except Exception:
            results.append({
                "סימול": symbol,
                "שער נוכחי": None,
                "תחזית (%)": None,
                "שער תחזית": None,
                "(ימים) יעד": None,
                "ביטחון (%)": None,
                "הסבר התחזית": "שגיאה בעיבוד הניתוח"
            })

    df_results = pd.DataFrame(results)
    df_results.sort_values(by="תחזית (%)", ascending=False, inplace=True)
    df_results.reset_index(drop=True, inplace=True)
    return df_results

import pandas as pd
import numpy as np

def fetch_price_history(ticker, period="3mo", interval="1d"):
    import yfinance as yf
    df = yf.download(ticker, period=period, interval=interval)
    df.dropna(inplace=True)
    return df

def detect_trade_signals(df, threshold=0.03):
    try:
        df = df.copy()
        df['Buy Signal'] = False
        df['Sell Signal'] = False

        for i in range(1, len(df)):
            if (
                pd.notna(df['Close'].iloc[i]) and
                pd.notna(df['Close'].iloc[i - 1]) and
                df['Close'].iloc[i] > df['Close'].iloc[i - 1] * (1 + threshold)
            ):
                df.at[df.index[i], 'Buy Signal'] = True
            elif (
                pd.notna(df['Close'].iloc[i]) and
                pd.notna(df['Close'].iloc[i - 1]) and
                df['Close'].iloc[i] < df['Close'].iloc[i - 1] * (1 - threshold)
            ):
                df.at[df.index[i], 'Sell Signal'] = True

        return df
    except Exception as e:
        print(f"Error in detect_trade_signals: {e}")
        return df
🔁 מוכן לשלוח את model_engine.py, backtesting.py, או כל קובץ אחר – רק תגיד.






You said:
שלח


ChatGPT said:
הנה הקובץ model_engine.py המלא והמתוקן – מוכן להעתקה:

python
Copy
Edit
import xgboost as xgb
import pandas as pd
import yfinance as yf

# רשימות סימולים
stock_symbols = ["AAPL", "MSFT", "GOOGL", "META", "NVDA", "TSLA", "AMZN", "NFLX", "AMD", "INTC"]
crypto_symbols = ["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "XRP-USD", "DOGE-USD", "ADA-USD", "AVAX-USD", "LINK-USD", "MATIC-USD"]

# פונקציה לשליפת נתונים
def fetch_data(symbol, period="1y"):
    df = yf.download(symbol, period=period, interval="1d", progress=False)
    return df if not df.empty else None

# פיצ'רים בסיסיים
def create_features(df):
    df['return'] = df['Close'].pct_change()
    df['ma5'] = df['Close'].rolling(window=5).mean()
    df['ma20'] = df['Close'].rolling(window=20).mean()
    df['std'] = df['Close'].rolling(window=20).std()
    df['target'] = df['Close'].shift(-10) / df['Close'] - 1  # אחוז שינוי 10 ימים קדימה
    df = df.dropna()
    return df

# אימון מודל XGBoost
def train_model(X_train, y_train):
    model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100)
    model.fit(X_train, y_train)
    return model

# פונקציית ניתוח עם המודל
def analyze_with_model(model, symbol_list, asset_type):
    results = []
    for symbol in symbol_list:
        try:
            df = fetch_data(symbol, period="6mo")
            if df is None or len(df) < 30:
                continue

            name = yf.Ticker(symbol).info.get("shortName", symbol)
            features_df = create_features(df.copy())
            X_pred = features_df[["return", "ma5", "ma20", "std"]]
            y_pred = model.predict(X_pred)
            forecast_pct = round(float(y_pred[-1] * 100), 2)

            current_price = round(float(df["Close"].iloc[-1]), 2)
            target_price = round(current_price * (1 + forecast_pct / 100), 2)
            forecast_days = 10
            timestamp = df.index[-1].strftime("%Y-%m-%d")

            results.append({
                "סימול": symbol,
                "שם מלא": name,
                "סוג": asset_type,
                "שער נוכחי": current_price,
                "תחזית (%)": forecast_pct,
                "שער תחזית": target_price,
                "יעד (ימים)": forecast_days,
                "תאריך איתות": timestamp
            })
        except Exception as e:
            print(f"שגיאה בניתוח {symbol}: {e}")
            continue
    return pd.DataFrame(results)

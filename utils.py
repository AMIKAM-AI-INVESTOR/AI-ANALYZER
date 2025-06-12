
import yfinance as yf
import pandas as pd

# שליפת היסטוריית מחירים
def fetch_price_history(symbol, period="6mo", interval="1d"):
    data = yf.download(symbol, period=period, interval=interval)
    if data.empty:
        raise ValueError(f"No data found for symbol: {symbol}")
    data.dropna(inplace=True)
    return data

# זיהוי אותות קנייה ומכירה פשוטים לפי שינוי באחוזים
def detect_trade_signals(df, threshold=0.03):
    if "Close" not in df.columns:
        raise ValueError("DataFrame does not contain 'Close' column.")

    signals = []
    for i in range(1, len(df)):
        try:
            if df["Close"].iloc[i] > df["Close"].iloc[i - 1] * (1 + threshold):
                signals.append("Buy")
            elif df["Close"].iloc[i] < df["Close"].iloc[i - 1] * (1 - threshold):
                signals.append("Sell")
            else:
                signals.append("")
        except Exception as e:
            signals.append("")
    signals.insert(0, "")  # עבור היום הראשון
    df["Signal"] = signals
    return df

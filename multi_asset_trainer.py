import yfinance as yf
import pandas as pd
from ai_model import train_basic_ai_model
from pattern_recognition import detect_head_and_shoulders, detect_flags

def train_on_multiple_symbols(symbols, period="6mo"):
    pattern_stats = []

    for symbol in symbols:
        df = yf.download(symbol, period=period)
        if df.empty or len(df) < 30:
            continue
        df.dropna(inplace=True)
        model = train_basic_ai_model(df)
        patterns = detect_head_and_shoulders(df) + detect_flags(df)

        for date, pattern_name in patterns:
            if date in df.index:
                price = df.loc[date]["Close"]
                future_data = df[df.index > date].head(5)
                success = any(future_data["Close"] > price * 1.03)
                pattern_stats.append({
                    "symbol": symbol,
                    "date": date,
                    "pattern": pattern_name,
                    "price": price,
                    "success": success
                })

    return pd.DataFrame(pattern_stats)

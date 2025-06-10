import yfinance as yf
import pandas as pd
import datetime

stock_symbols = ["AAPL", "NVDA", "TSLA", "AMZN", "META", "MSFT", "GOOGL", "ON", "COST", "AMD"]
crypto_symbols = ["BTC-USD", "ETH-USD", "SOL-USD", "AVAX-USD", "BNB-USD", "ADA-USD", "XRP-USD", "DOGE-USD", "LTC-USD", "MATIC-USD"]

def get_top10_predictions():
    today = datetime.datetime.today().date()
    end_date = today
    start_date = today - datetime.timedelta(days=90)

    def analyze(symbols, asset_type):
        predictions = []
        for symbol in symbols:
            try:
                df = yf.download(symbol, start=start_date, end=end_date)
                if df.empty or 'Close' not in df.columns:
                    continue
                change = (df['Close'].iloc[-1] - df['Close'].iloc[0]) / df['Close'].iloc[0]
                target_days = int((end_date - start_date).days)
                predictions.append({
                    "symbol": symbol,
                    "expected_change": f"{round(change * 100)}%",
                    "target_time": f"{target_days} ימים"
                })
            except Exception as e:
                print(f"Error processing {symbol}: {e}")
        return pd.DataFrame([{"type": asset_type, **row} for _, row in pd.DataFrame(predictions).iterrows()])

    stock_df = analyze(stock_symbols, "Stock")
    crypto_df = analyze(crypto_symbols, "Crypto")
    return pd.concat([stock_df, crypto_df], ignore_index=True)

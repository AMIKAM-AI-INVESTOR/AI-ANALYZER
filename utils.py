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

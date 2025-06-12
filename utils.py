
import pandas as pd

def detect_trade_signals(df, threshold=0.03):
    signals = ['Hold']
    for i in range(1, len(df)):
        if pd.notna(df['Close'].iloc[i]) and pd.notna(df['Close'].iloc[i - 1]):
            if df['Close'].iloc[i] > df['Close'].iloc[i - 1] * (1 + threshold):
                signals.append('Buy')
            elif df['Close'].iloc[i] < df['Close'].iloc[i - 1] * (1 - threshold):
                signals.append('Sell')
            else:
                signals.append('Hold')
        else:
            signals.append('Hold')
    df['Signal'] = signals
    return df

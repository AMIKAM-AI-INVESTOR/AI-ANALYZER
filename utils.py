# utils.py
import pandas as pd

def detect_trade_signals(df, threshold=0.03):
    """
    Adds a 'Signal' column to the DataFrame based on simple price change logic:
    Buy if price rises above threshold, sell if falls below threshold.
    """
    signals = []
    for i in range(1, len(df)):
        prev_close = df['Close'].iloc[i - 1]
        curr_close = df['Close'].iloc[i]
        if curr_close > prev_close * (1 + threshold):
            signals.append('Buy')
        elif curr_close < prev_close * (1 - threshold):
            signals.append('Sell')
        else:
            signals.append('')

    signals.insert(0, '')  # First row has no signal
    df['Signal'] = signals
    return df

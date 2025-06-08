# modules/utils.py
import yfinance as yf
import pandas as pd

def get_data(symbol):
    try:
        df = yf.download(symbol, period='1y')
        if 'Close' not in df:
            return None
        return df
    except:
        return None
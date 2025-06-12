import pandas as pd

def get_top10_forecasts():
    try:
        stocks_df = pd.read_csv("top10_stocks_forecast.csv")
        crypto_df = pd.read_csv("top10_crypto_forecast.csv")
        return stocks_df, crypto_df
    except Exception as e:
        print(f"Error loading top10 files: {e}")
        return pd.DataFrame(), pd.DataFrame()

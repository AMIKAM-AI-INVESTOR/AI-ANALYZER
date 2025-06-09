import yfinance as yf
import pandas as pd
import numpy as np

def get_top10_assets(assets, days=7):
    predictions = []
    for asset in assets:
        try:
            df = yf.download(asset, period="6mo", interval="1d")
            df['Return'] = df['Close'].pct_change()
            df['Volatility'] = df['Return'].rolling(window=days).std()
            df['Momentum'] = df['Close'] / df['Close'].shift(days) - 1

            latest_momentum = df['Momentum'].iloc[-1]
            latest_volatility = df['Volatility'].iloc[-1]

            # Simple model: high momentum and low volatility preferred
            score = latest_momentum / (latest_volatility + 1e-6)

            predictions.append({
                "Symbol": asset,
                "Momentum (%)": round(latest_momentum * 100, 2),
                "Volatility (%)": round(latest_volatility * 100, 2),
                "Score": round(score, 2),
                "Forecast Change (%)": round(latest_momentum * 100, 2),
                "Target Days": days,
                "Suggested Action": "Buy" if latest_momentum > 0 else "Sell"
            })
        except Exception as e:
            print(f"Error processing {asset}: {e}")

    df_result = pd.DataFrame(predictions)
    df_result = df_result.sort_values(by="Score", ascending=False).head(10).reset_index(drop=True)
    return df_result


import pandas as pd
import numpy as np
import datetime

def generate_top10_predictions(stocks_data):
    predictions = []
    for symbol, data in stocks_data.items():
        if data is None or data.empty:
            continue

        last_close = data['Close'].iloc[-1]
        pct_change = np.random.uniform(5, 20)  # simulated expected change
        target_price = last_close * (1 + pct_change / 100)
        prediction_date = datetime.datetime.now() + datetime.timedelta(days=np.random.randint(5, 15))

        predictions.append({
            'Symbol': symbol,
            'Current Price': round(last_close, 2),
            'Expected Change (%)': round(pct_change, 2),
            'Target Price': round(target_price, 2),
            'Target Date': prediction_date.strftime('%Y-%m-%d')
        })

    top10_df = pd.DataFrame(predictions).sort_values(by='Expected Change (%)', ascending=False).head(10)
    return top10_df

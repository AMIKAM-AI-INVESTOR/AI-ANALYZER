
import pandas as pd

def get_top10_forecasts():
    top10_stocks_df = pd.DataFrame({
        "Symbol": ["AAPL", "TSLA"],
        "Name": ["Apple", "Tesla"],
        "Current Price": [199.27, 324.23],
        "Predicted Change (%)": [8.2, 12.5],
        "Target Price": [215.61, 364.76],
        "Target Time": ["7d", "5d"],
        "Confidence": [0.92, 0.88],
        "Forecast Explanation (Hebrew)": [
            "תבנית טכנית חזקה + מגמה שורית.",
            "איתות פריצה טכני + נפחים גבוהים."
        ]
    })

    top10_crypto_df = pd.DataFrame({
        "Symbol": ["BTC-USD", "ETH-USD"],
        "Name": ["Bitcoin", "Ethereum"],
        "Current Price": [108281.27, 2765.06],
        "Predicted Change (%)": [22.7, 18.9],
        "Target Price": [132861.12, 3287.66],
        "Target Time": ["3d", "4d"],
        "Confidence": [0.97, 0.95],
        "Forecast Explanation (Hebrew)": [
            "זיהוי תבנית שורית + גידול בביקושים.",
            "נתונים חזקים מהמולקציה + פריצה טכנית."
        ]
    })

    return top10_stocks_df, top10_crypto_df

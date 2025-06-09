import pandas as pd

def get_top10_assets():
    # Example structure – replace with real analysis logic or data source
    top10_stocks = pd.DataFrame([
        {"Symbol": "AAPL", "Name": "Apple Inc.", "Expected Change (%)": 12.5, "Target Days": 30},
        {"Symbol": "MSFT", "Name": "Microsoft Corp.", "Expected Change (%)": 10.3, "Target Days": 45},
        {"Symbol": "GOOGL", "Name": "Alphabet Inc.", "Expected Change (%)": 9.8, "Target Days": 40},
        {"Symbol": "NVDA", "Name": "NVIDIA Corp.", "Expected Change (%)": 15.0, "Target Days": 25},
        {"Symbol": "AMZN", "Name": "Amazon.com Inc.", "Expected Change (%)": 11.2, "Target Days": 35},
        {"Symbol": "TSLA", "Name": "Tesla Inc.", "Expected Change (%)": 13.7, "Target Days": 28},
        {"Symbol": "META", "Name": "Meta Platforms Inc.", "Expected Change (%)": 8.5, "Target Days": 33},
        {"Symbol": "ON", "Name": "ON Semiconductor", "Expected Change (%)": 14.1, "Target Days": 27},
        {"Symbol": "ADBE", "Name": "Adobe Inc.", "Expected Change (%)": 9.4, "Target Days": 36},
        {"Symbol": "AMD", "Name": "Advanced Micro Devices", "Expected Change (%)": 12.9, "Target Days": 31},
    ])

    top10_crypto = pd.DataFrame([
        {"Symbol": "BTC-USD", "Name": "Bitcoin", "Expected Change (%)": 6.2, "Target Days": 15},
        {"Symbol": "ETH-USD", "Name": "Ethereum", "Expected Change (%)": 5.7, "Target Days": 18},
        {"Symbol": "SOL-USD", "Name": "Solana", "Expected Change (%)": 7.9, "Target Days": 12},
        {"Symbol": "ADA-USD", "Name": "Cardano", "Expected Change (%)": 8.5, "Target Days": 20},
        {"Symbol": "XRP-USD", "Name": "XRP", "Expected Change (%)": 4.1, "Target Days": 14},
        {"Symbol": "AVAX-USD", "Name": "Avalanche", "Expected Change (%)": 6.7, "Target Days": 16},
        {"Symbol": "DOT-USD", "Name": "Polkadot", "Expected Change (%)": 5.8, "Target Days": 19},
        {"Symbol": "DOGE-USD", "Name": "Dogecoin", "Expected Change (%)": 6.5, "Target Days": 13},
        {"Symbol": "MATIC-USD", "Name": "Polygon", "Expected Change (%)": 7.2, "Target Days": 17},
        {"Symbol": "LINK-USD", "Name": "Chainlink", "Expected Change (%)": 8.0, "Target Days": 21},
    ])

    return top10_stocks, top10_crypto

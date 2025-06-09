import yfinance as yf

def get_fundamental_data(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info

        keys_to_extract = [
            'longName', 'sector', 'industry', 'country',
            'marketCap', 'enterpriseValue', 'trailingPE',
            'forwardPE', 'priceToBook', 'pegRatio',
            'dividendYield', 'beta', 'profitMargins',
            'grossMargins', 'operatingMargins',
            'returnOnEquity', 'returnOnAssets',
            'revenueGrowth', 'earningsGrowth', 'currentRatio',
            'quickRatio', 'debtToEquity'
        ]

        extracted_info = {k: info[k] for k in keys_to_extract if k in info}
        return extracted_info

    except Exception as e:
        return {"error": str(e)}

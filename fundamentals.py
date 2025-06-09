import yfinance as yf

def fetch_fundamentals(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        return {
            "Market Cap": info.get("marketCap", "N/A"),
            "PE Ratio": info.get("trailingPE", "N/A"),
            "EPS": info.get("trailingEps", "N/A"),
            "Dividend Yield": info.get("dividendYield", "N/A"),
            "52 Week High": info.get("fiftyTwoWeekHigh", "N/A"),
            "52 Week Low": info.get("fiftyTwoWeekLow", "N/A"),
            "Beta": info.get("beta", "N/A"),
            "Sector": info.get("sector", "N/A"),
            "Industry": info.get("industry", "N/A"),
        }
    except Exception as e:
        print(f"Error fetching fundamentals for {ticker_symbol}: {e}")
        return {
            "Market Cap": "N/A",
            "PE Ratio": "N/A",
            "EPS": "N/A",
            "Dividend Yield": "N/A",
            "52 Week High": "N/A",
            "52 Week Low": "N/A",
            "Beta": "N/A",
            "Sector": "N/A",
            "Industry": "N/A",
        }

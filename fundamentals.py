import yfinance as yf
import pandas as pd

def get_fundamental_data(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info

        data = {
            "Company Name": info.get("longName", "N/A"),
            "Sector": info.get("sector", "N/A"),
            "Industry": info.get("industry", "N/A"),
            "Market Cap": info.get("marketCap", "N/A"),
            "Trailing P/E": info.get("trailingPE", "N/A"),
            "Forward P/E": info.get("forwardPE", "N/A"),
            "PEG Ratio": info.get("pegRatio", "N/A"),
            "Price to Book": info.get("priceToBook", "N/A"),
            "Dividend Yield": info.get("dividendYield", "N/A"),
            "Beta": info.get("beta", "N/A"),
            "52 Week High": info.get("fiftyTwoWeekHigh", "N/A"),
            "52 Week Low": info.get("fiftyTwoWeekLow", "N/A"),
            "Average Volume": info.get("averageVolume", "N/A"),
            "EPS (TTM)": info.get("trailingEps", "N/A"),
            "Revenue": info.get("totalRevenue", "N/A"),
            "Gross Margins": info.get("grossMargins", "N/A"),
            "Operating Margins": info.get("operatingMargins", "N/A"),
            "Profit Margins": info.get("profitMargins", "N/A"),
        }

        return pd.DataFrame(list(data.items()), columns=["Metric", "Value"])

    except Exception as e:
        print(f"Error fetching fundamental data for {ticker_symbol}: {e}")
        return pd.DataFrame(columns=["Metric", "Value"])

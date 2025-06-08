import yfinance as yf
import pandas as pd


def get_fundamentals(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info

        return {
            "Market Cap": info.get("marketCap"),
            "Trailing P/E": info.get("trailingPE"),
            "Forward P/E": info.get("forwardPE"),
            "PEG Ratio": info.get("pegRatio"),
            "Price/Sales": info.get("priceToSalesTrailing12Months"),
            "Price/Book": info.get("priceToBook"),
            "Dividend Yield": info.get("dividendYield"),
            "Beta": info.get("beta"),
            "52 Week High": info.get("fiftyTwoWeekHigh"),
            "52 Week Low": info.get("fiftyTwoWeekLow"),
            "EPS (TTM)": info.get("trailingEps"),
            "Earnings Growth": info.get("earningsQuarterlyGrowth"),
            "Revenue Growth": info.get("revenueQuarterlyGrowth"),
        }
    except Exception as e:
        return {"error": str(e)}

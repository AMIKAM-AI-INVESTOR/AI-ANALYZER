
import pandas as pd
import yfinance as yf
import requests
from datetime import datetime
from bs4 import BeautifulSoup

# מקור ראשי: yfinance
def fetch_from_yfinance(symbol, period="6mo", interval="1d"):
    try:
        df = yf.download(symbol, period=period, interval=interval)
        if not df.empty and all(col in df.columns for col in ["Open", "High", "Low", "Close"]):
            df.dropna(inplace=True)
            return df
    except Exception:
        return None
    return None

# מקור שני: CoinGecko (לקריפטו)
def fetch_from_coingecko(symbol):
    symbol = symbol.lower().replace("-usd", "")
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{symbol}/market_chart"
        params = {"vs_currency": "usd", "days": "180", "interval": "daily"}
        response = requests.get(url, params=params)
        data = response.json()
        if "prices" in data:
            df = pd.DataFrame(data["prices"], columns=["timestamp", "Close"])
            df["Date"] = pd.to_datetime(df["timestamp"], unit="ms")
            df["Close"] = df["Close"].astype(float)
            df["Open"] = df["Close"]
            df["High"] = df["Close"]
            df["Low"] = df["Close"]
            df["Volume"] = 0
            df.set_index("Date", inplace=True)
            return df[["Open", "High", "Low", "Close", "Volume"]]
    except Exception:
        return None
    return None

# מקור שלישי: Alpha Vantage
def fetch_from_alpha_vantage(symbol, apikey="demo"):
    try:
        url = ("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED"
               f"&symbol={symbol}&outputsize=compact&apikey={apikey}")
        response = requests.get(url)
        data = response.json()
        if "Time Series (Daily)" in data:
            records = []
            for date_str, values in data["Time Series (Daily)"].items():
                records.append({
                    "Date": pd.to_datetime(date_str),
                    "Open": float(values["1. open"]),
                    "High": float(values["2. high"]),
                    "Low": float(values["3. low"]),
                    "Close": float(values["4. close"]),
                    "Volume": float(values["6. volume"])
                })
            df = pd.DataFrame(records)
            df.set_index("Date", inplace=True)
            return df.sort_index()
    except Exception:
        return None
    return None

# מקור רביעי: Finviz (מידע יומי בלבד, לא היסטורי)
def fetch_from_finviz(symbol):
    try:
        url = f"https://finviz.com/quote.ashx?t={symbol}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", class_="snapshot-table2")
        rows = table.find_all("tr")
        price = None
        for row in rows:
            cells = row.find_all("td")
            for i in range(0, len(cells), 2):
                key = cells[i].text
                val = cells[i + 1].text
                if key == "Price":
                    price = float(val.replace(",", ""))
        if price:
            date = pd.to_datetime("today").normalize()
            df = pd.DataFrame({
                "Open": [price],
                "High": [price],
                "Low": [price],
                "Close": [price],
                "Volume": [0]
            }, index=[date])
            return df
    except Exception:
        return None
    return None

# מקור חמישי: Investing (לא רשמי, ייתכן שיחסם)
def fetch_from_investing(symbol):
    try:
        symbol_map = {
            "AAPL": "apple-computer-inc",
            "TSLA": "tesla-motors",
            "MSFT": "microsoft-corp"
        }
        if symbol not in symbol_map:
            return None
        url = f"https://www.investing.com/equities/{symbol_map[symbol]}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        span = soup.find("span", attrs={"data-test": "instrument-price-last"})
        if span:
            price = float(span.text.replace(",", ""))
            date = pd.to_datetime("today").normalize()
            df = pd.DataFrame({
                "Open": [price],
                "High": [price],
                "Low": [price],
                "Close": [price],
                "Volume": [0]
            }, index=[date])
            return df
    except Exception:
        return None
    return None

# מנוע ראשי: שילוב המקורות לפי סדר
def fetch_price_history(symbol, period="6mo", interval="1d"):
    for fetcher in [
        fetch_from_yfinance,
        fetch_from_coingecko,
        fetch_from_alpha_vantage,
        fetch_from_finviz,
        fetch_from_investing,
    ]:
        df = fetcher(symbol)
        if df is not None and not df.empty:
            return df
    return pd.DataFrame()

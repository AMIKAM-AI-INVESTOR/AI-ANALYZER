import requests
from bs4 import BeautifulSoup

def get_fundamental_data(symbol):
    try:
        url = f"https://finance.yahoo.com/quote/{symbol}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        data = {}
        for row in soup.find_all("tr"):
            cols = row.find_all("td")
            if len(cols) == 2:
                key = cols[0].text.strip()
                value = cols[1].text.strip()
                data[key] = value

        # נבחר פרטים מרכזיים להצגה
        keys_of_interest = [
            "Market Cap", "PE Ratio (TTM)", "EPS (TTM)",
            "Forward Dividend & Yield", "Previous Close", "Open"
        ]
        filtered_data = {k: data[k] for k in keys_of_interest if k in data}

        return filtered_data
    except Exception as e:
        return {"Error": str(e)}

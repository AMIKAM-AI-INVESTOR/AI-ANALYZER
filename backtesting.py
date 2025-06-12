import pandas as pd

def run_backtesting(df):
    df = df.copy()
    df = df.dropna(subset=['Signal'])

    buy_signals = df[df['Signal'] == 'Buy']
    sell_signals = df[df['Signal'] == 'Sell']

    trades = []
    position = None

    for idx, row in df.iterrows():
        if row['Signal'] == 'Buy' and position is None:
            position = (idx, row['Close'])
        elif row['Signal'] == 'Sell' and position:
            buy_date, buy_price = position
            sell_price = row['Close']
            return_pct = ((sell_price - buy_price) / buy_price) * 100
            trades.append({
                "Buy Date": buy_date,
                "Sell Date": idx,
                "Buy Price": buy_price,
                "Sell Price": sell_price,
                "Return (%)": round(return_pct, 2)
            })
            position = None

    return pd.DataFrame(trades)

def run_backtesting(df, signals):
    results = []
    for date, signal in signals:
        entry_price = df.loc[date]["Close"]
        future_data = df[df.index > date].head(5)  # טווח בדיקה: 5 ימים קדימה
        success = any(future_data["Close"] > entry_price * 1.03) if signal == "Buy" else any(future_data["Close"] < entry_price * 0.97)
        results.append({
            "date": date,
            "signal": signal,
            "entry_price": entry_price,
            "success": success
        })
    return pd.DataFrame(results)

import pandas as pd

def backtest_signals(df):
    df = df.copy()
    positions = []
    trades = []

    for i in range(len(df)):
        if df['Signal'].iloc[i] == 'Buy':
            positions.append((df.index[i], df['Close'].iloc[i]))
        elif df['Signal'].iloc[i] == 'Sell' and positions:
            buy_date, buy_price = positions.pop(0)
            sell_date = df.index[i]
            sell_price = df['Close'].iloc[i]
            return_pct = ((sell_price - buy_price) / buy_price) * 100
            trades.append({
                "Buy Date": buy_date,
                "Sell Date": sell_date,
                "Buy Price": buy_price,
                "Sell Price": sell_price,
                "Return (%)": round(return_pct, 2)
            })

    return pd.DataFrame(trades)

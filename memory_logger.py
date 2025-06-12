
import pandas as pd
import os

def log_pattern_result(symbol, date, pattern, entry_price, success, pct_change, file_path="memory_log.csv"):
    new_row = {
        "symbol": symbol,
        "date": date,
        "pattern": pattern,
        "entry_price": entry_price,
        "success": success,
        "pct_change": round(pct_change * 100, 2)
    }

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        df = pd.DataFrame([new_row])

    df.to_csv(file_path, index=False)

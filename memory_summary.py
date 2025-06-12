
import pandas as pd
import os

def summarize_memory(file_path="memory_log.csv"):
    if not os.path.exists(file_path):
        return pd.DataFrame()

    df = pd.read_csv(file_path)
    summary = df.groupby("pattern").agg(
        total_signals=("success", "count"),
        success_rate=("success", "mean"),
        avg_pct_change=("pct_change", "mean")
    ).reset_index()

    summary["success_rate"] = (summary["success_rate"] * 100).round(2)
    summary["avg_pct_change"] = summary["avg_pct_change"].round(2)
    return summary.sort_values(by="success_rate", ascending=False)

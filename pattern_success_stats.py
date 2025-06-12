
import pandas as pd

def summarize_pattern_stats(df):
    summary = df.groupby("pattern")["success"].agg(["count", "mean"]).reset_index()
    summary.columns = ["Pattern", "Total Occurrences", "Success Rate"]
    summary["Success Rate"] = (summary["Success Rate"] * 100).round(2)
    return summary.sort_values(by="Success Rate", ascending=False)

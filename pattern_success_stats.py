def summarize_pattern_stats(df):
    return df.groupby("pattern")["success"].agg(["count", "mean"]).rename(columns={"count": "Total", "mean": "Success Rate (%)"})

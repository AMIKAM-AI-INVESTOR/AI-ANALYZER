import pandas as pd
import numpy as np

def detect_head_and_shoulders(df):
    # דוגמה לזיהוי ראש וכתפיים פשוט
    signals = []
    for i in range(2, len(df)-2):
        left_shoulder = df['High'].iloc[i-2]
        head = df['High'].iloc[i]
        right_shoulder = df['High'].iloc[i+2]
        if head > left_shoulder and head > right_shoulder and abs(left_shoulder - right_shoulder) / head < 0.1:
            signals.append((df.index[i], "Head & Shoulders"))
    return signals

def detect_flags(df):
    # תבנית דגל שורי/דובי פשוטה – קווי מגמה
    signals = []
    for i in range(10, len(df)):
        recent = df['Close'].iloc[i-10:i]
        trend = recent.diff().mean()
        if trend > 0.3:
            signals.append((df.index[i], "Bull Flag"))
        elif trend < -0.3:
            signals.append((df.index[i], "Bear Flag"))
    return signals

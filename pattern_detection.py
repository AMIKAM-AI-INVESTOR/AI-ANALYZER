
import pandas as pd

def detect_patterns(df):
    patterns = []

    # דוגמה בסיסית לזיהוי תבנית "ראש וכתפיים" על בסיס תנודות במחיר
    highs = df['High']
    for i in range(2, len(highs) - 2):
        left = highs[i - 2]
        center = highs[i]
        right = highs[i + 2]
        if center > left and center > right:
            if abs(left - right) / center < 0.1:  # שתי הכתפיים באותו גובה בערך
                patterns.append({'type': 'ראש וכתפיים', 'index': df.index[i]})

    # דוגמה לתבנית "דגל שורי": עלייה חדה ואחריה תעלה יורדת קצרה
    df['slope'] = df['Close'].diff()
    for i in range(10, len(df) - 5):
        uptrend = df['slope'].iloc[i-10:i].mean()
        flag = df['slope'].iloc[i:i+5].mean()
        if uptrend > 1 and flag < 0:
            patterns.append({'type': 'דגל שורי', 'index': df.index[i+2]})

    return patterns

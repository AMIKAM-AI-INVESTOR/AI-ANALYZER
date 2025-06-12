import pandas as pd
import numpy as np

def generate_explanation(df):
    try:
        latest_close = df['Close'].iloc[-1] if not df['Close'].empty else np.nan
        ma5 = df['ma5'].iloc[-1] if not df['ma5'].empty else np.nan
        ma20 = df['ma20'].iloc[-1] if not df['ma20'].empty else np.nan
        std = df['std'].iloc[-1] if not df['std'].empty else np.nan
    except Exception:
        return "שגיאה בקריאת הנתונים"

    explanation_parts = []

    if (isinstance(latest_close, (int, float, np.float64)) and
        isinstance(ma5, (int, float, np.float64)) and
        isinstance(ma20, (int, float, np.float64)) and
        not pd.isna(latest_close) and
        not pd.isna(ma5) and
        not pd.isna(ma20)):
        
        if latest_close > ma5 > ma20:
            explanation_parts.append("מגמת עלייה (MA5 > MA20)")
        elif latest_close < ma5 < ma20:
            explanation_parts.append("מגמת ירידה (MA5 < MA20)")
        else:
            explanation_parts.append("אין מגמה ברורה")
    else:
        explanation_parts.append("נתונים חלקיים לממוצעים")

    if (isinstance(std, (int, float, np.float64)) and
        isinstance(latest_close, (int, float, np.float64)) and
        not pd.isna(std) and
        not pd.isna(latest_close)):
        
        if std < 0.02 * latest_close:
            explanation_parts.append("תנודתיות נמוכה")
        else:
            explanation_parts.append("תנודתיות גבוהה")
    else:
        explanation_parts.append("אין מספיק מידע על תנודתיות")

    return " | ".join(explanation_parts)

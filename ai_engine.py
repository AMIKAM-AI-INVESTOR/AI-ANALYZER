
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# יצירת תכונות גרפיות בסיסיות
def create_features(df):
    df['Return_1d'] = df['Close'].pct_change()
    df['Return_5d'] = df['Close'].pct_change(5)
    df['MA_5'] = df['Close'].rolling(window=5).mean()
    df['MA_20'] = df['Close'].rolling(window=20).mean()
    df['Volatility_5d'] = df['Close'].rolling(window=5).std()
    df['Volume_Change'] = df['Volume'].pct_change()
    df = df.dropna()
    return df

# יצירת טווח מטרה עתידי (% שינוי)
def add_target(df, future_days=5):
    df['Target_Change'] = df['Close'].shift(-future_days) / df['Close'] - 1
    df = df.dropna()
    return df

# אימון מודל XGBoost והחזרת תחזית (לשימוש בדוחות ו-Top10)
def train_predict_xgb(df):
    df = create_features(df)
    df = add_target(df)

    features = ['Return_1d', 'Return_5d', 'MA_5', 'MA_20', 'Volatility_5d', 'Volume_Change']
    X = df[features]
    y = df['Target_Change']

    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.2)

    model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
    model.fit(X_train, y_train)

    prediction = model.predict([X.iloc[-1]])[0]
    mae = mean_absolute_error(y_test, model.predict(X_test))

    return prediction * 100, 1 - mae  # אחוז שינוי חזוי + ביטחון מקורב

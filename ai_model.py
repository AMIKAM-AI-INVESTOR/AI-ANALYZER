from sklearn.tree import DecisionTreeClassifier

def train_basic_ai_model(df):
    df['target'] = df['Close'].shift(-3) > df['Close']
    df = df.dropna()
    X = df[['Open', 'High', 'Low', 'Close', 'Volume']]
    y = df['target'].astype(int)
    
    model = DecisionTreeClassifier(max_depth=5)
    model.fit(X, y)
    return model

def predict_signal(model, df):
    last_row = df[['Open', 'High', 'Low', 'Close', 'Volume']].iloc[-1:]
    prediction = model.predict(last_row)[0]
    return "Buy" if prediction == 1 else "Sell"

from sklearn.ensemble import RandomForestRegressor

def build_random_forest_model():
    return RandomForestRegressor(n_estimators=100)

def predict_short_term_trend(asset, data, lookback_days=30):
    X = data[['Open', 'High', 'Low', 'Volume']].values[-lookback_days:]
    y = data['Close'].values[-lookback_days+1:]
    
    model = build_random_forest_model()
    
    model.fit(X[:-1], y)
    
    last_data = X[-1].reshape(1, -1)
    
    prediction = model.predict(last_data)[0]
    
    return prediction
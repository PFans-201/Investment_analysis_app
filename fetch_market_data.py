import yfinance as yf
import pandas as pd

def fetch_data(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    data['daily_return'] = data['Adj Close'].pct_change()
    data['moving_average'] = data['Adj Close'].rolling(window=50).mean()
    data['volatility'] = data['daily_return'].rolling(window=50).std()
    return data.dropna()

def fetch_multiple_assets(symbols, start_date, end_date):
    return {symbol: fetch_data(symbol, start_date, end_date) for symbol in symbols}
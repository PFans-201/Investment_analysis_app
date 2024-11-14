import pandas as pd
import yfinance as yf
import numpy as np

def get_initial_asset_universe():
    sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    nasdaq100 = pd.read_html('https://en.wikipedia.org/wiki/Nasdaq-100')[4]
    
    url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1'
    crypto_data = pd.read_json(url)
    
    return sp500['Symbol'].tolist(), nasdaq100['Ticker'].tolist(), crypto_data['id'].tolist()

def filter_assets(symbols):
    filtered_symbols = []
    for symbol in symbols:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        if (info.get('averageVolume', 0) > 1000000 and info.get('marketCap', 0) > 1000000000):
            filtered_symbols.append(symbol)
    
    return filtered_symbols

def analyze_asset_performance(symbols, lookback_period='1y'):
    performance_data = []
    
    for symbol in symbols:
        data = yf.download(symbol, period=lookback_period)
        returns = data['Adj Close'].pct_change()
        performance_data.append({
            'symbol': symbol,
            'return': returns.mean() * 252,
            'volatility': returns.std() * np.sqrt(252),
            'sharpe_ratio': (returns.mean() * 252) / (returns.std() * np.sqrt(252))
        })
    
    return pd.DataFrame(performance_data)

def correlation_based_selection(symbols, max_correlation=0.7):
    data = yf.download(symbols, period='1y')['Adj Close']
    correlation_matrix = data.pct_change().corr()
    
    selected_assets = [symbols[0]]
    
    for symbol in symbols[1:]:
        if all(abs(correlation_matrix.loc[symbol, selected]) < max_correlation for selected in selected_assets):
            selected_assets.append(symbol)
    
    return selected_assets

def get_tracked_assets(client, dataset_id, table_id):
    query = f"""
    SELECT symbol, asset_type
    FROM `{dataset_id}.{table_id}`
    """
    return client.query(query).to_dataframe()
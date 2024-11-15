import numpy as np
import matplotlib.pyplot as plt
import json

# Load user configuration
with open("data/user_config.json") as f:
    config = json.load(f)

def portfolio_optimization(returns, risk_tolerance):
    risk_tolerance = config['risk_tolerance']
    num_assets = len(returns.columns)
    num_portfolios = 10000
    results = np.zeros((3, num_portfolios))
    
    # Get asset allocation based on risk tolerance
    allocation = config['asset_allocation'][risk_tolerance]
    
    for i in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)
        
        # Adjust weights based on risk tolerance
        for j, asset_type in enumerate(allocation.keys()):
            weights[j] = allocation[asset_type] + np.random.normal(0, 0.05)  # Add some randomness
        
        weights /= np.sum(weights)  # Normalize weights
        
        portfolio_return = np.sum(weights * returns.mean() * 252)
        portfolio_stddev = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))
        
        results[0,i] = portfolio_return
        results[1,i] = portfolio_stddev
        results[2,i] = results[0,i] / results[1,i]  # Sharpe ratio
    
    max_sharpe_idx = np.argmax(results[2])
    sdp, rp = results[1, max_sharpe_idx], results[0, max_sharpe_idx]
    
    return {'Return': rp, 'Volatility': sdp, 'Weights': weights}

def apply_stop_loss_take_profit(portfolio_value, initial_value):
    stop_loss = initial_value * (1 - config['stop_loss_percentage'])
    take_profit = initial_value * (1 + config['take_profit_percentage'])
    
    if portfolio_value <= stop_loss:
        print("Stop-loss triggered. Reallocating to safer assets.")
        return 'stop_loss'
    elif portfolio_value >= take_profit:
        print("Take-profit triggered. Realizing gains and rebalancing.")
        return 'take_profit'
    return None

def rebalance_portfolio(portfolio, target_allocation):
    total_value = sum(portfolio.values())
    rebalanced_portfolio = {}
    for asset, target_weight in target_allocation.items():
        target_value = total_value * target_weight
        rebalanced_portfolio[asset] = target_value
    return rebalanced_portfolio

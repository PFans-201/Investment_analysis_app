import numpy as np
import matplotlib.pyplot as plt

def portfolio_optimization(returns):
    num_assets = len(returns.columns)
    num_portfolios = 10000
    
    results = np.zeros((3, num_portfolios))
    
    for i in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)
        
        portfolio_return = np.sum(weights * returns.mean() * 252)
        portfolio_stddev = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))
        
        results[0,i] = portfolio_return
        results[1,i] = portfolio_stddev
        results[2,i] = results[0,i] / results[1,i]  # Sharpe ratio
    
    max_sharpe_idx = np.argmax(results[2])
    
    sdp, rp = results[1,max_sharpe_idx], results[0,max_sharpe_idx]
    
    plt.scatter(results[1,:], results[0,:], c=results[2,:], cmap='viridis')
    plt.colorbar(label='Sharpe Ratio')
    
    plt.scatter(sdp, rp, marker='*', color='r', s=100)
    
    plt.savefig('output/efficient_frontier.png')
    plt.close()
    
    return {'Return': rp, 'Volatility': sdp}
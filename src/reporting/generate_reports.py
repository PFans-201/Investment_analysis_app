import pandas as pd 
import matplotlib.pyplot as plt 

def generate_performance_report(portfolio_df , optimal_allocation): 
     # Save portfolio performance to CSV 
     portfolio_df.to_csv("output/portfolio_performance.csv", index=False)

     # Save optimal allocation to CSV 
     pd.DataFrame(optimal_allocation , index=[0]).to_csv("output/optimal_allocation.csv", index=False)

     # Generate performance plot 
     plt.figure(figsize=(10 ,6)) 
     plt.plot(portfolio_df['date'], portfolio_df['value']) 
     plt.title('Portfolio Value Over Time') 
     plt.xlabel('Date') 
     plt.ylabel('Portfolio Value (€)') 
     plt.savefig('output/portfolio_performance.png') 
     plt.close()

     # Print summary statistics 
     print("\nPortfolio Performance Summary:") 
     print(f"Total Return: {(portfolio_df['value'].iloc[-1] / portfolio_df['value'].iloc[0] - 1) * 100:.2f}%") 
     print(f"Annualized Return: {((portfolio_df['value'].iloc[-1] / portfolio_df['value'].iloc[0]) ** (12 / len(portfolio_df)) - 1) * 100:.2f}%") 
     print(f"Sharpe Ratio: {portfolio_df['value'].pct_change().mean() / portfolio_df['value'].pct_change().std() * (252 ** 0.5):.2f}")  
     print(f"Maximum Drawdown: {(portfolio_df['value'] / portfolio_df['value'].cummax() - 1).min() * 100:.2f}%")
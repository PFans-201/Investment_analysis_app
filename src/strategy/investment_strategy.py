import json
import pandas as pd

with open('data/user_config.json') as f:
    config = json.load(f)

def evaluate_and_adjust_strategy(portfolio_df):
    monthly_investment = config["initial_monthly_investment"]
    max_investment = config["max_monthly_investment"]
    
    evaluation_frequency = config["strategy_adjustment_trigger"]["evaluation_frequency_months"]
    
    performance_met, portfolio_return, drawdown = assess_performance(portfolio_df)
    
    current_month = len(portfolio_df)
    
    if current_month % evaluation_frequency == 0:
        if performance_met:
            monthly_investment *= min(max_investment / monthly_investment , 1.1) 
            print(f"Increasing monthly investment to {monthly_investment:.2f}€")
        else:
            print("Adjusting risk tolerance due to underperformance")
            
            # Logic to adjust risk tolerance can be added here
    
     # Return the adjusted monthly investment amount.
     return monthly_investment 

def assess_performance(portfolio_df):
     portfolio_df["monthly_return"] = portfolio_df["value"].pct_change()
     portfolio_return = portfolio_df["monthly_return"].mean()
     drawdown = (portfolio_df["value"] / portfolio_df["value"].cummax() - 1).min()
     
     performance_met = (
         portfolio_return >= config["strategy_adjustment_trigger"]["min_return_threshold"]
         and drawdown >= config["strategy_adjustment_trigger"]["max_drawdown_threshold"]
     )
     
     return performance_met, portfolio_return, drawdown 
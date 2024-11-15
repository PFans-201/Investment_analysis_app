import schedule
import time
from datetime import datetime, timedelta
import pandas as pd
import pyodbc
from src.data_acquisition import fetch_market_data, asset_selection
from src.data_processing import preprocess_data
from src.models import lstm_model, random_forest_model
from src.portfolio_optimization import efficient_frontier
from src.strategy import investment_strategy
from src.alerts import real_time_alerts
from src.reporting import generate_reports
from google.cloud import bigquery
import json

with open('data/user_config.json') as f:
    config = json.load(f)

def store_monthly_summary(portfolio_df, optimal_allocation):
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=your_server.database.windows.net;DATABASE=your_database;UID=your_username;PWD=your_password')
    cursor = conn.cursor()

    latest_data = portfolio_df.iloc[-1]
    month_end = latest_data['date']
    portfolio_value = latest_data['value']
    monthly_return = portfolio_df['value'].pct_change().iloc[-1]

    cursor.execute("""
    INSERT INTO monthly_summaries (month_end, portfolio_value, monthly_return, stock_allocation, crypto_allocation)
    VALUES (?, ?, ?, ?, ?)
    """, month_end, portfolio_value, monthly_return, optimal_allocation['stock'], optimal_allocation['crypto'])

    conn.commit()
    conn.close()

def run_daily_analysis():
    client = bigquery.Client()
    tracked_assets = asset_selection.get_tracked_assets(
        client, 
        config['bigquery']['dataset_id'], 
        config['bigquery']['table_id']
    )

    long_term_start = '2010-01-01'
    short_term_start = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')

    long_term_data = fetch_market_data.fetch_multiple_assets(tracked_assets['symbol'].tolist(), long_term_start, end_date)
    short_term_data = fetch_market_data.fetch_multiple_assets(tracked_assets['symbol'].tolist(), short_term_start, end_date)

    # Prepare data and train models for each asset
    models = {}
    for symbol in tracked_assets['symbol']:
        if symbol in long_term_data and symbol in short_term_data:
            try:
                X_long, y_long, scaler_long = preprocess_data.prepare_lstm_data(long_term_data[symbol])
                X_short, y_short, scaler_short = preprocess_data.prepare_lstm_data(short_term_data[symbol])

                model_long = lstm_model.build_lstm_model((X_long.shape[1], 1))
                model_long.fit(X_long, y_long, epochs=50, batch_size=32)

                model_short = lstm_model.build_lstm_model((X_short.shape[1], 1))
                model_short.set_weights(model_long.get_weights())
                model_short.fit(X_short, y_short, epochs=25, batch_size=32)

                models[symbol] = {
                    'model': model_short,
                    'scaler': scaler_short,
                    'X': X_short
                }
            except Exception as e:
                print(f"Error processing data for {symbol}: {str(e)}")
        else:
            print(f"Skipping {symbol} due to missing data in long-term or short-term dataset.")

    portfolio_value = config["initial_monthly_investment"]
    portfolio_df = pd.DataFrame(columns=["date", "value"])


    for month in range(1, config["investment_horizon_months"] + 1):
        monthly_investment = investment_strategy.evaluate_and_adjust_strategy(portfolio_df, month)

        # Apply risk tolerance factor
        risk_factor = 1.0
        if config["risk_tolerance"] == "low":
            risk_factor = 0.8
        elif config["risk_tolerance"] == "medium":
            risk_factor = 1.0
        elif config["risk_tolerance"] == "high":
            risk_factor = 1.2

        # Predict returns for each asset and calculate weighted return
        predicted_returns = {}
        for symbol, model_data in models.items():
            predicted_return = lstm_model.predict_return(model_data['model'], model_data['X'][-1], model_data['scaler'])
            predicted_returns[symbol] = predicted_return * risk_factor

        # Use the latest optimal allocation for weighted return calculation
        if 'optimal_allocation' in locals():
            weighted_return = sum(optimal_allocation[symbol] * predicted_returns[symbol] for symbol in optimal_allocation)
        else:
            weighted_return = sum(predicted_returns.values()) / len(predicted_returns)

        portfolio_value += monthly_investment
        portfolio_value *= (1 + weighted_return)

        portfolio_df = portfolio_df.append({
            "date": pd.Timestamp.now() + pd.DateOffset(months=month),
            "value": portfolio_value
        }, ignore_index=True)

        # Recalculate optimal allocation monthly
        returns = pd.DataFrame({symbol: data['daily_return'] for symbol, data in short_term_data.items()})
        optimal_allocation = efficient_frontier.portfolio_optimization(returns)

        # Generate and store monthly summary
        if month % 1 == 0:  # Every month
            generate_reports.generate_performance_report(portfolio_df, optimal_allocation)
            store_monthly_summary(portfolio_df, optimal_allocation)

    # Set up and check alerts
    alert_thresholds = [
        real_time_alerts.set_alert_thresholds(symbol, asset_type)
        for symbol, asset_type in zip(tracked_assets['symbol'], tracked_assets['asset_type'])
    ]
    real_time_alerts.check_price_movements(alert_thresholds)
    real_time_alerts.check_predictive_alerts(alert_thresholds)

# Schedule the daily analysis
schedule.every().day.at("00:00").do(run_daily_analysis)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
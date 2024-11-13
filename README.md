# Investment Analysis App

This application provides a comprehensive investment analysis tool for stocks and cryptocurrencies. It includes features such as automated asset selection, predictive modeling, portfolio optimization, and real-time alerts.

## Setup

1. Clone the repository
2. Install the required packages:

`pip install -r requirements.txt`

3. Set up a Google Cloud project and BigQuery dataset
4. Configure the `data/user_config.json` file with your preferences and API keys
5. Run `scripts/update_asset_list.py` to initialize your tracked assets
6. Run `main.py` to start the daily analysis and alert system

7. Recommended organization:
<pre>
investment-analysis-app/
├── data/
│   └── user_config.json
├── src/
│   ├── data_acquisition/
│   │   ├── __init__.py
│   │   ├── fetch_market_data.py
│   │   └── asset_selection.py
│   ├── data_processing/
│   │   ├── __init__.py
│   │   └── preprocess_data.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── lstm_model.py
│   │   └── random_forest_model.py
│   ├── portfolio_optimization/
│   │   ├── __init__.py
│   │   └── efficient_frontier.py
│   ├── strategy/
│   │   ├── __init__.py
│   │   └── investment_strategy.py
│   ├── alerts/
│   │   ├── __init__.py
│   │   └── real_time_alerts.py
│   └── reporting/
│       ├── __init__.py
│       └── generate_reports.py
├── scripts/
│   └── update_asset_list.py
├── main.py
├── requirements.txt
└── README.md
</pre>

## Features

- Automated asset selection based on performance and correlation
- LSTM and Random Forest models for price prediction
- Portfolio optimization using the Efficient Frontier
- Dynamic strategy adjustment based on performance
- Real-time price movement and predictive alerts
- Monthly performance reporting and data storage in SQL database
- Integration with Power BI for visualization (setup required)

## File Structure

- `data/`: Contains configuration files and raw data
- `src/`: Source code for all main functionalities
- `scripts/`: Utility scripts for maintenance tasks
- `main.py`: Main script to run the daily analysis
- `requirements.txt`: List of required Python packages
- `README.md`: This file

## Usage

After setup, the application will run daily analyses automatically. You can modify the schedule in `main.py` if needed. Check the `output/` directory for generated reports and the SQL database for stored monthly summaries.

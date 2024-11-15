# Investment Analysis App

This application provides a comprehensive investment analysis tool for a variety of asset classes, including stocks, cryptocurrencies, bonds, REITs, commodities, and more. It features automated asset selection, predictive modeling, portfolio optimization, and real-time alerts to help users make informed investment decisions.

## Setup

1. Clone the repository
`git clone https://github.com/PFans-201/Investment_analysis_app.git` next `cd investment-analysis-app`

2. Install the required packages:

`pip install -r requirements.txt`

3. Set up a Google Cloud project and BigQuery dataset
4. <b>Configure</b> the `data/user_config.json` file with your preferences and API keys
5. <b>Run</b> `scripts/update_asset_list.py` to initialize your tracked assets
6. <b>Run</b> `main.py` to start the daily analysis and alert system

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

- <b>Automated Asset Selection:</b> Based on performance metrics and correlation analysis across various asset classes.
- <b>Predictive Modeling:</b> Utilizes LSTM and Random Forest models for price prediction of stocks, bonds, REITs, commodities, and cryptocurrencies.
- <b>Portfolio Optimization:</b> Employs algorithms like the Efficient Frontier to calculate optimal allocations for maximizing returns based on user-defined risk tolerance.
- <b>Dynamic Strategy Adjustment:</b> Regularly adjusts investment strategies based on performance metrics such as Sharpe Ratio and drawdown.
- <b>Real-time Alerts:</b> Monitors price movements and market conditions to send predictive alerts.
- <b>Monthly Performance Reporting:</b> Generates detailed reports on portfolio performance and strategic adjustments.
- <b>Integration with Power BI:</b> For advanced visualization and insights (setup required).

## Usage

After setup, the application will run daily analyses automatically. You can modify the schedule in main.py if needed. Check the output/ directory for generated reports and the SQL database for stored monthly summaries.

## Example Workflow
- Fetch historical market data for multiple asset classes (stocks, bonds, REITs, commodities).
- Apply predictive models to forecast future prices.
- Optimize portfolio allocations using the Efficient Frontier method.
- Adjust monthly investments dynamically based on performance metrics.
- Generate automated reports summarizing performance and strategic adjustments.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/PFans-201/Investment_analysis_app/blob/main/LICENSE) file for details.

##  Additional Considerations
To ensure that your app can handle a broader range of assets effectively:
- <b>Data Acquisition:</b> Ensure your fetch_market_data.py can retrieve data for all specified asset types (e.g., bonds, REITs).
- <b>Modeling Enhancements:</b> Consider implementing additional machine learning models that suit different asset classes (e.g., ARIMA for bonds).
- <b>User Configuration:</b> Update user_config.json to allow users to specify which assets they want to track or invest in.


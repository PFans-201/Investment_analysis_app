# investment-analysis-app/src/__init__.py

# Data Acquisition: 
# Place the following files in the 'data_acquisition' folder
from .fetch_market_data import fetch_data, fetch_multiple_assets
from .asset_selection import get_initial_asset_universe, filter_assets, analyze_asset_performance, correlation_based_selection, get_tracked_assets

# Data Processing:
# Place the following file in the 'data_processing' folder
from .preprocess_data import prepare_lstm_data

# Models:
# Place the following files in the 'models' folder
from .lstm_model import build_lstm_model
from .random_forest_model import build_random_forest_model, predict_short_term_trend

# Portfolio Optimization:
# Place the following file in the 'portfolio_optimization' folder
from .efficient_frontier import portfolio_optimization

# Strategy:
# Place the following file in the 'strategy' folder
from .investment_strategy import evaluate_and_adjust_strategy, assess_performance

# Alerts:
# Place the following file in the 'alerts' folder
from .real_time_alerts import set_alert_thresholds, check_price_movements, check_predictive_alerts, send_alert

# Reporting:
# Place the following file in the 'reporting' folder
from .generate_reports import generate_performance_report

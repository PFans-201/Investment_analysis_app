import yfinance as yf 
from src.models.random_forest_model import predict_short_term_trend 

def set_alert_thresholds(asset, asset_type):
    if asset_type == 'stock':
        return {
            'asset': asset,
            'upper_threshold': config['alert_thresholds']['stock_upper'],
            'lower_threshold': config['alert_thresholds']['stock_lower']
        }
    elif asset_type == 'crypto':
        return {
            'asset': asset,
            'upper_threshold': config['alert_thresholds']['crypto_upper'],
            'lower_threshold': config['alert_thresholds']['crypto_lower']
        }

def check_price_movements(alert_thresholds): 
     for threshold in alert_thresholds: 
         asset=threshold['asset'] 
         data=yf.download(asset , period="2d") 
         price_change=(data['Close'][-1]-data['Close'][0])/data['Close'][0]

         if price_change >= threshold['upper_threshold']: 
             send_alert(f"{asset} has increased by {price_change:.2%}. Consider taking profits.") 
         elif price_change <= threshold['lower_threshold']: 
             send_alert(f"{asset} has decreased by {price_change:.2%}. Consider buying the dip.")

def check_predictive_alerts(alert_thresholds): 
     for threshold in alert_thresholds: 
         asset=threshold['asset'] 
         data=yf.download(asset , period="31d") 
         current_price=data['Close'][-1] 
         predicted_price=predict_short_term_trend(asset , data) 
         predicted_change=(predicted_price-current_price)/current_price 

         if predicted_change >= threshold['upper_threshold']: 
             send_alert(f"Prediction: {asset} may increase by {predicted_change:.2%}. Consider buying.") 
         elif predicted_change <= threshold['lower_threshold']: 
             send_alert(f"Prediction: {asset} may decrease by {predicted_change:.2%}. Consider selling.")

def send_alert(message): 
     print(f"ALERT: {message}") # Implement your preferred alert method here (e.g., email or push notification)
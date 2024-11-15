from google.cloud import bigquery  
from src.data_acquisition.asset_selection import get_initial_asset_universe , filter_assets , analyze_asset_performance , correlation_based_selection  
import pandas as pd  
from datetime import datetime  
import json  

with open('data/user_config.json') as f:  
      config=json.load(f)  

def update_asset_list():  
      # Get initial asset universe  
      sp500_symbols , nasdaq100_symbols , crypto_symbols=get_initial_asset_universe()  

      # Filter assets  
      filtered_stocks=filter_assets(sp500_symbols + nasdaq100_symbols , 'stock')  
      filtered_cryptos=filter_assets(crypto_symbols , 'crypto')  

      # Analyze performance  
      stock_performance=analyze_asset_performance(filtered_stocks , 'stock')  
      crypto_performance=analyze_asset_performance(filtered_cryptos , 'crypto')  

      # Select top performers based on Sharpe ratio  
      top_stocks=stock_performance.nlargest(50 , 'sharpe_ratio')['symbol'].tolist()  
      top_cryptos=crypto_performance.nlargest(20 , 'sharpe_ratio')['symbol'].tolist()  

      # Perform correlation-based selection  
      diverse_stocks=correlation_based_selection(top_stocks)  
      diverse_cryptos=correlation_based_selection(top_cryptos)  

      # Prepare data for BigQuery  
      updated_assets=(  
          [{'symbol': symbol , 'asset_type': 'stock'} for symbol in diverse_stocks] +  
          [{'symbol': symbol , 'asset_type': 'crypto'} for symbol in diverse_cryptos]  
      )  

      # Update BigQuery table  
      client=bigquery.Client()  
      table_id=f"{config['bigquery']['project_id']}.{config['bigquery']['dataset_id']}.{config['bigquery']['table_id']}"  

      job_config=bigquery.LoadJobConfig(  
          write_disposition="WRITE_TRUNCATE",  
          schema=[  
              bigquery.SchemaField("symbol" , "STRING"),  
              bigquery.SchemaField("asset_type" , "STRING"),  
              bigquery.SchemaField("last_updated" , "TIMESTAMP"),  
          ],  
      )  

      df=pd.DataFrame(updated_assets)  
      df['last_updated']=datetime.now()  

      job=client.load_table_from_dataframe(df , table_id , job_config=job_config)  
      job.result()  

      print(f"Updated asset list in BigQuery: {len(diverse_stocks)} stocks and {len(diverse_cryptos)} cryptocurrencies")  

if __name__ == "__main__":  
      update_asset_list()  
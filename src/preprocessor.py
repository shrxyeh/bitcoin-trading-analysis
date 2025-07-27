import pandas as pd
import numpy as np
import pytz
from datetime import datetime

class DataPreprocessor:
    def __init__(self):
        pass
    
    def preprocess_trader_data(self, df):
        """Preprocess trader data with correct date parsing"""
        # Standardize column names
        df.columns = df.columns.str.replace(' ', '_').str.lower()
        
        print("\nRaw timestamp samples:")
        if 'timestamp_ist' in df.columns:
            print(df['timestamp_ist'].head(3))
        
        # Handle IST timestamp parsing
        if 'timestamp_ist' in df.columns:
            try:
                # Parse with dayfirst=True for DD-MM-YYYY format
                df['timestamp'] = pd.to_datetime(
                    df['timestamp_ist'],
                    dayfirst=True,
                    format='%d-%m-%Y %H:%M'
                )
                # Convert IST to UTC
                df['timestamp'] = df['timestamp'].dt.tz_localize('Asia/Kolkata').dt.tz_convert('UTC')
                df['date'] = df['timestamp'].dt.date
            except Exception as e:
                print(f"Date parsing error: {e}")
                raise ValueError("Failed to parse timestamps. Check date format in raw data.")
        
        # Handle missing values
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        df[numeric_columns] = df[numeric_columns].fillna(0)
        
        # Create additional features
        if 'closed_pnl' in df.columns:
            df['is_profitable'] = df['closed_pnl'] > 0
            df['abs_pnl'] = abs(df['closed_pnl'])
        
        if 'size_usd' in df.columns:
            df['trade_value'] = df['size_usd']
        elif 'size_tokens' in df.columns and 'execution_price' in df.columns:
            df['trade_value'] = df['size_tokens'] * df['execution_price']
        
        # Standardize column names
        column_mapping = {
            'account': 'account',
            'coin': 'symbol',
            'execution_price': 'execution_price',
            'size_tokens': 'size',
            'size_usd': 'size_usd',
            'closed_pnl': 'closedPnL',
            'side': 'side'
        }
        
        existing_mapping = {k: v for k, v in column_mapping.items() if k in df.columns}
        df = df.rename(columns=existing_mapping)
        
        print(f"\nTrader date range: {df['date'].min()} to {df['date'].max()}")
        return df
    
    def preprocess_sentiment_data(self, df):
        """Preprocess sentiment data with epoch time handling"""
        df.columns = df.columns.str.replace(' ', '_').str.lower()
        
        # Handle epoch time conversion (seconds since 1970)
        if 'timestamp' in df.columns:
            try:
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
                df['date'] = df['timestamp'].dt.date
            except:
                raise ValueError("Failed to convert sentiment timestamps")
        
        # Create numerical sentiment score
        if 'classification' in df.columns:
            sentiment_map = {
                'Fear': -1,
                'Greed': 1,
                'Neutral': 0,
                'Extreme Fear': -2,
                'Extreme Greed': 2
            }
            df['Classification'] = df['classification'].str.strip().str.title()
            df['sentiment_score'] = df['Classification'].map(sentiment_map).fillna(0)
        
        print(f"\nSentiment date range: {df['date'].min()} to {df['date'].max()}")
        return df
    
    def merge_datasets(self, trader_df, sentiment_df):
        """Merge datasets with validation"""
        print("\nPreprocessing trader data...")
        trader_df = self.preprocess_trader_data(trader_df.copy())
        
        print("\nPreprocessing sentiment data...")
        sentiment_df = self.preprocess_sentiment_data(sentiment_df.copy())
        
        merged_df = pd.merge(
            trader_df,
            sentiment_df[['date', 'Classification', 'sentiment_score']],
            on='date',
            how='left',
            indicator=True
        )
        
        merge_stats = merged_df['_merge'].value_counts()
        print("\nMerge results:")
        print(merge_stats)
        
        if merge_stats.get('both', 0) == 0:
            raise ValueError("No dates matched between datasets")
        
        merged_df = merged_df.drop(columns='_merge')
        print(f"\nFinal merged data shape: {merged_df.shape}")
        return merged_df
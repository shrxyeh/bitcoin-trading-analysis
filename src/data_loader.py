import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class DataLoader:
    def __init__(self, trader_data_path, sentiment_data_path):
        self.trader_data_path = trader_data_path
        self.sentiment_data_path = sentiment_data_path
    
    def load_trader_data(self):
        """Load trader data with timestamp inspection"""
        try:
            df = pd.read_csv(self.trader_data_path)
            print(f"\nTrader data loaded: {df.shape}")
            
            # Inspect timestamp columns
            ts_cols = [c for c in df.columns if 'time' in c.lower() or 'date' in c.lower()]
            print("Timestamp columns:", ts_cols)
            if ts_cols:
                print("Sample values:")
                print(df[ts_cols[0]].head(3))
            
            return df
        except Exception as e:
            raise ValueError(f"Failed to load trader data: {str(e)}")
    
    def load_sentiment_data(self):
        """Load sentiment data"""
        try:
            df = pd.read_csv(self.sentiment_data_path)
            print(f"\nSentiment data loaded: {df.shape}")
            
            # Inspect date columns
            date_cols = [c for c in df.columns if 'date' in c.lower() or 'time' in c.lower()]
            if date_cols:
                print("Sample dates:")
                print(df[date_cols[0]].head(3))
            
            return df
        except Exception as e:
            raise ValueError(f"Failed to load sentiment data: {str(e)}")
    
    def load_all_data(self):
        """Load both datasets"""
        trader_data = self.load_trader_data()
        sentiment_data = self.load_sentiment_data()
        return trader_data, sentiment_data
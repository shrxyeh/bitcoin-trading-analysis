import pandas as pd
import numpy as np

def inspect_data():
    print("=== DATA INSPECTION ===\n")
    
    print("TRADER DATA:")
    print("-" * 40)
    try:
        trader_data = pd.read_csv('data/raw/historical_trader_data.csv')
        print(f"Shape: {trader_data.shape}")
        print(f"Columns: {list(trader_data.columns)}")
        print(f"Data types:\n{trader_data.dtypes}")
        print(f"\nFirst 3 rows:")
        print(trader_data.head(3))
        print(f"\nSample of numeric columns:")
        numeric_cols = trader_data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            print(trader_data[numeric_cols].describe())
        
        # Check for PnL column variations
        pnl_columns = [col for col in trader_data.columns if 'pnl' in col.lower() or 'profit' in col.lower()]
        print(f"\nPossible PnL columns: {pnl_columns}")
        
        # Check for timestamp columns
        time_columns = [col for col in trader_data.columns if 'time' in col.lower() or 'date' in col.lower()]
        print(f"Time-related columns: {time_columns}")
        
    except FileNotFoundError:
        print("Trader data file not found. Please ensure the file is in data/raw/historical_trader_data.csv")
    except Exception as e:
        print(f"Error loading trader data: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # Load and inspect sentiment data
    print("SENTIMENT DATA:")
    print("-" * 40)
    try:
        sentiment_data = pd.read_csv('data/raw/fear_greed_index.csv')
        print(f"Shape: {sentiment_data.shape}")
        print(f"Columns: {list(sentiment_data.columns)}")
        print(f"Data types:\n{sentiment_data.dtypes}")
        print(f"\nFirst 3 rows:")
        print(sentiment_data.head(3))
        
        classification_cols = [col for col in sentiment_data.columns if 'class' in col.lower() or 'sentiment' in col.lower()]
        print(f"\nPossible classification columns: {classification_cols}")
        
        if len(classification_cols) > 0:
            main_class_col = classification_cols[0]
            print(f"\nUnique values in {main_class_col}:")
            print(sentiment_data[main_class_col].value_counts())
        
        # Check for date columns
        date_columns = [col for col in sentiment_data.columns if 'date' in col.lower() or 'time' in col.lower()]
        print(f"Date-related columns: {date_columns}")
        
    except FileNotFoundError:
        print("Sentiment data file not found. Please ensure the file is in data/raw/fear_greed_index.csv")
    except Exception as e:
        print(f"Error loading sentiment data: {e}")
    
    print("\n" + "="*60 + "\n")
    print("RECOMMENDATIONS:")
    print("1. Check if column names match what the code expects")
    print("2. Verify date formats are consistent between datasets") 
    print("3. Ensure PnL and classification columns are properly named")
    print("4. Run this inspection before running main.py")

if __name__ == "__main__":
    inspect_data()
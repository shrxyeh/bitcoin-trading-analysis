import pandas as pd
import numpy as np
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

class TradingAnalyzer:
    def __init__(self):
        self.scaler = StandardScaler()
    
    def calculate_trader_metrics(self, df):
        """Calculate key trader performance metrics"""
        # Check which columns are actually available
        available_metrics = {
            'closedPnL': ['sum', 'mean', 'std', 'count'],
            'trade_value': ['sum', 'mean'],
            'is_profitable': 'mean'
        }
        
        metrics_to_calculate = {
            col: agg for col, agg in available_metrics.items()
            if col in df.columns
        }
        
        if not metrics_to_calculate:
            raise ValueError("No valid columns found for metric calculation")
            
        trader_metrics = df.groupby('account').agg(metrics_to_calculate).round(4)
        
        # Flatten column names
        trader_metrics.columns = ['_'.join(col).strip() for col in trader_metrics.columns]
        trader_metrics = trader_metrics.reset_index()
        
        # Calculate additional metrics
        if 'closedPnL_mean' in trader_metrics.columns and 'closedPnL_std' in trader_metrics.columns:
            trader_metrics['sharpe_ratio'] = trader_metrics['closedPnL_mean'] / trader_metrics['closedPnL_std'].replace(0, np.nan)
        
        if 'is_profitable_mean' in trader_metrics.columns:
            trader_metrics['win_rate'] = trader_metrics['is_profitable_mean']
            
        if 'closedPnL_sum' in trader_metrics.columns:
            trader_metrics['total_pnl'] = trader_metrics['closedPnL_sum']
            
        if 'closedPnL_mean' in trader_metrics.columns:
            trader_metrics['avg_pnl'] = trader_metrics['closedPnL_mean']
            
        if 'closedPnL_count' in trader_metrics.columns:
            trader_metrics['trade_count'] = trader_metrics['closedPnL_count']
        
        return trader_metrics
    
    def sentiment_performance_analysis(self, df):
        """Analyze performance by market sentiment"""
        if 'Classification' not in df.columns:
            raise ValueError("Classification column not found for sentiment analysis")
            
        available_metrics = {
            'closedPnL': ['mean', 'sum', 'std'],
            'trade_value': 'mean',
            'is_profitable': 'mean'
        }
        
        # Only include columns that exist in the dataframe
        metrics_to_calculate = {
            col: agg for col, agg in available_metrics.items()
            if col in df.columns
        }
        
        if not metrics_to_calculate:
            raise ValueError("No valid columns found for sentiment analysis")
            
        sentiment_analysis = df.groupby('Classification').agg(metrics_to_calculate).round(4)
        
        return sentiment_analysis
    
    def correlation_analysis(self, df):
        """Perform correlation analysis"""
        potential_cols = ['closedPnL', 'size', 'size_usd', 'sentiment_score', 'trade_value', 'fee']
        available_cols = [col for col in potential_cols if col in df.columns]
        
        if len(available_cols) < 2:
            print("Not enough numeric columns for correlation analysis")
            return pd.DataFrame()
            
        correlation_matrix = df[available_cols].corr()
        return correlation_matrix
    
    def cluster_traders(self, trader_metrics, n_clusters=3):
        """Cluster traders based on performance metrics"""
        if not isinstance(trader_metrics, pd.DataFrame) or trader_metrics.empty:
            raise ValueError("Invalid input data for clustering")
            
        potential_features = ['total_pnl', 'win_rate', 'trade_count', 'avg_pnl', 'closedPnL_sum', 'closedPnL_mean']
        available_features = [col for col in potential_features if col in trader_metrics.columns]
        
        if len(available_features) < 2:
            print(f"Not enough features for clustering (available: {available_features})")
            trader_metrics['cluster'] = 0  
            return trader_metrics
        
        try:
            X = self.scaler.fit_transform(trader_metrics[available_features])
            
            # Perform clustering
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            trader_metrics['cluster'] = kmeans.fit_predict(X)
        except Exception as e:
            print(f"Clustering failed: {str(e)}")
            trader_metrics['cluster'] = 0 
            
        return trader_metrics
    
    def statistical_tests(self, df):
        """Perform statistical tests"""
        results = {}
        
        if 'Classification' not in df.columns or 'closedPnL' not in df.columns:
            return results
            
        # T-test for PnL difference between Fear and Greed
        try:
            fear_pnl = df[df['Classification'] == 'Fear']['closedPnL'].dropna()
            greed_pnl = df[df['Classification'] == 'Greed']['closedPnL'].dropna()
            
            if len(fear_pnl) > 1 and len(greed_pnl) > 1:
                t_stat, p_value = stats.ttest_ind(fear_pnl, greed_pnl)
                results['pnl_ttest'] = {
                    't_statistic': t_stat,
                    'p_value': p_value,
                    'significant': p_value < 0.05
                }
        except Exception as e:
            print(f"Statistical test failed: {str(e)}")
        
        return results
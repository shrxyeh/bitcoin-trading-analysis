import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

class DataVisualizer:
    def __init__(self):
        # Updated style setting for newer Seaborn versions
        try:
            sns.set_theme(style='whitegrid')
        except:
            plt.style.use('ggplot')
        self.output_dir = 'data/outputs'
        os.makedirs(self.output_dir, exist_ok=True)

    def plot_sentiment_distribution(self, data):
        """Plot distribution of sentiment classifications"""
        if 'Classification' not in data.columns:
            print("No sentiment data available for visualization")
            return
        
        plt.figure(figsize=(10, 6))
        data['Classification'].value_counts().plot(kind='bar', color=sns.color_palette("viridis"))
        plt.title('Market Sentiment Distribution')
        plt.xlabel('Sentiment Class')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/sentiment_distribution.png')
        plt.close()

    def plot_trader_performance(self, metrics):
        """Visualize trader performance metrics"""
        required_cols = ['total_pnl', 'win_rate', 'trade_count']
        if not all(col in metrics.columns for col in required_cols):
            print("Missing required columns for trader performance plot")
            return
        
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        
        sns.histplot(data=metrics, x='total_pnl', ax=axes[0], bins=50, kde=True)
        axes[0].set_title('Profit Distribution')
        
        sns.histplot(data=metrics, x='win_rate', ax=axes[1], bins=20, kde=True)
        axes[1].set_title('Win Rate Distribution')
        
        sns.histplot(data=metrics, x='trade_count', ax=axes[2], bins=50, kde=True)
        axes[2].set_title('Trade Count Distribution')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/trader_performance.png')
        plt.close()

    def plot_correlation_heatmap(self, data):
        """Generate correlation heatmap"""
        numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
        if len(numeric_cols) < 2:
            print("Not enough numeric columns for correlation")
            return
        
        plt.figure(figsize=(12, 8))
        corr = data[numeric_cols].corr()
        sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', center=0)
        plt.title('Feature Correlation Heatmap')
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/correlation_heatmap.png')
        plt.close()

    def plot_cluster_analysis(self, metrics):
        """Visualize trader clusters if available"""
        if 'cluster' not in metrics.columns:
            print("No cluster data available")
            return
        
        plt.figure(figsize=(10, 6))
        sns.scatterplot(
            data=metrics,
            x='total_pnl',
            y='win_rate',
            hue='cluster',
            palette='viridis',
            size='trade_count',
            sizes=(20, 200),
            alpha=0.7
        )
        plt.title('Trader Clusters by Performance')
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/cluster_analysis.png')
        plt.close()

    def generate_all_visualizations(self, merged_data, trader_metrics, correlation_matrix=None):
        """Generate all visualizations"""
        try:
            self.plot_sentiment_distribution(merged_data)
            self.plot_trader_performance(trader_metrics)
            
            if correlation_matrix is not None:
                self.plot_correlation_heatmap(correlation_matrix)
            
            self.plot_cluster_analysis(trader_metrics)
            return True
        except Exception as e:
            print(f"Visualization error: {str(e)}")
            return False
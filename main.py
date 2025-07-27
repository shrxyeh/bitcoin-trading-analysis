import sys
import os
import pandas as pd
from src.data_loader import DataLoader
from src.preprocessor import DataPreprocessor
from src.analyzer import TradingAnalyzer
from src.visualizer import DataVisualizer

def main():
    print("=== Bitcoin Trading Analysis Project ===\n")
    
    try:
        print("Initializing components...")
        loader = DataLoader(
            trader_data_path='data/raw/historical_data.csv',
            sentiment_data_path='data/raw/fear_greed_index.csv'
        )
        preprocessor = DataPreprocessor()
        analyzer = TradingAnalyzer()
        visualizer = DataVisualizer()
        
        print("\n1. Loading data...")
        trader_data, sentiment_data = loader.load_all_data()
        
        if trader_data is None or sentiment_data is None:
            raise ValueError("Failed to load data files. Check file paths and formats.")
        
        print("\n2. Preprocessing and merging data...")
        merged_data = preprocessor.merge_datasets(trader_data, sentiment_data)
        
        os.makedirs('data/processed', exist_ok=True)
        merged_data.to_csv('data/processed/merged_data.csv', index=False)
        print(f"\nMerged data saved. Shape: {merged_data.shape}")
        
        print("\n3. Calculating trader performance metrics...")
        trader_metrics = analyzer.calculate_trader_metrics(merged_data)
        
        os.makedirs('data/outputs', exist_ok=True)
        trader_metrics.to_csv('data/outputs/trader_metrics.csv', index=False)
        print(f"Analyzed {len(trader_metrics)} unique traders")
        
        print("\n4. Analyzing performance by sentiment...")
        sentiment_performance = analyzer.sentiment_performance_analysis(merged_data)
        if not sentiment_performance.empty:
            print("\nPerformance by Sentiment:")
            print(sentiment_performance.to_markdown())
        else:
            print("No valid sentiment classification data available")
        
        print("\n5. Performing correlation analysis...")
        correlation_matrix = analyzer.correlation_analysis(merged_data)
        if correlation_matrix is not None:
            print("\nTop Correlations:")
            print(correlation_matrix.unstack().sort_values(ascending=False).drop_duplicates().head(10))
        
        print("\n6. Running statistical tests...")
        test_results = analyzer.statistical_tests(merged_data)
        if test_results:
            print("\nStatistical Test Results:")
            for test, result in test_results.items():
                print(f"{test}: {result}")
        
        print("\n7. Clustering traders...")
        trader_metrics = analyzer.cluster_traders(trader_metrics)
        if 'cluster' in trader_metrics.columns:
            print(f"Created {trader_metrics['cluster'].nunique()} trader clusters")
        
        print("\n8. Generating visualizations...")
        try:
            visualization_success = visualizer.generate_all_visualizations(
                merged_data=merged_data,
                trader_metrics=trader_metrics,
                correlation_matrix=correlation_matrix if 'correlation_matrix' in locals() else None
            )
            if visualization_success:
                print("Visualizations successfully saved to data/outputs/")
            else:
                print("Some visualizations failed to generate")
        except Exception as e:
            print(f"Visualization system error: {str(e)}")
        
        print("\n9. Generating summary report...")
        generate_summary_report(merged_data, trader_metrics, sentiment_performance, test_results)
        
    except Exception as e:
        print(f"\nError during analysis: {str(e)}")
        print("\nTroubleshooting tips:")
        print("- Verify all input files exist in data/raw/")
        print("- Check that timestamps are formatted correctly")
        print("- Ensure all required packages are installed (pandas, matplotlib, seaborn)")
        print("- Try running: pip install --upgrade matplotlib seaborn")
        return

    print("\n=== Analysis Complete! ===")
    print("Results saved to:")
    print("- data/processed/merged_data.csv")
    print("- data/outputs/ (visualizations and metrics)")

def generate_summary_report(merged_data, trader_metrics, sentiment_performance, test_results):
    """Generate comprehensive analysis report"""
    try:
        report_path = 'data/outputs/analysis_report.txt'
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w') as f:
            f.write("BITCOIN TRADING ANALYSIS REPORT\n")
            f.write("="*50 + "\n\n")
            
            f.write("1. DATA OVERVIEW\n")
            f.write("-"*50 + "\n")
            f.write(f"Analysis Period: {merged_data['date'].min()} to {merged_data['date'].max()}\n")
            f.write(f"Total Trades Analyzed: {len(merged_data):,}\n")
            f.write(f"Unique Traders: {len(trader_metrics):,}\n\n")
            
            f.write("2. MARKET SENTIMENT ANALYSIS\n")
            f.write("-"*50 + "\n")
            if not sentiment_performance.empty:
                f.write("Performance by Sentiment Class:\n\n")
                f.write(sentiment_performance.to_string())
                best_sentiment = sentiment_performance['closedPnL']['mean'].idxmax()
                f.write(f"\n\nBest Performing Sentiment: {best_sentiment}\n")
                f.write(f"Worst Performing Sentiment: {sentiment_performance['closedPnL']['mean'].idxmin()}\n")
            else:
                f.write("No sentiment data available\n")
            f.write("\n")
            
            f.write("3. TRADER PERFORMANCE\n")
            f.write("-"*50 + "\n")
            if not trader_metrics.empty:
                # Top Performers
                f.write("Top 5 Performing Traders:\n\n")
                top_traders = trader_metrics.nlargest(5, 'total_pnl')
                f.write(top_traders[['account', 'total_pnl', 'win_rate', 'trade_count']].to_string())
                
                # Performance Stats
                f.write("\n\nOverall Performance Statistics:\n")
                f.write(f"Average PnL: {trader_metrics['total_pnl'].mean():.2f}\n")
                f.write(f"Median Win Rate: {trader_metrics['win_rate'].median():.2%}\n")
                f.write(f"Most Active Trader: {trader_metrics.nlargest(1, 'trade_count')['account'].values[0]} "
                       f"({trader_metrics['trade_count'].max()} trades)\n")
            else:
                f.write("No trader metrics available\n")
            f.write("\n")
            
            f.write("4. STATISTICAL FINDINGS\n")
            f.write("-"*50 + "\n")
            if test_results:
                for test, result in test_results.items():
                    f.write(f"{test.upper()}:\n")
                    f.write(f"  - {result}\n")
            else:
                f.write("No statistical test results available\n")
            
            f.write("\n5. RECOMMENDATIONS & INSIGHTS\n")
            f.write("-"*50 + "\n")
            if not sentiment_performance.empty:
                best_sentiment = sentiment_performance['closedPnL']['mean'].idxmax()
                f.write(f"- Strategies performed best during {best_sentiment} market conditions\n")
            
            if 'cluster' in trader_metrics.columns:
                cluster_stats = trader_metrics.groupby('cluster')['total_pnl'].describe()
                f.write("\nTrader Cluster Insights:\n")
                f.write(cluster_stats.to_string())
                f.write("\n- Consider analyzing successful cluster patterns\n")
            
            f.write("\n- Review top performers for replicable strategies\n")
            f.write("- Examine correlation heatmap for significant relationships\n")
        
        print(f"Summary report saved to {report_path}")
    except Exception as e:
        print(f"Error generating report: {str(e)}")

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    main()
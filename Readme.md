
# Bitcoin Trading Analysis Project

![Bitcoin Trading](https://img.icons8.com/color/96/000000/bitcoin--v1.png)

##  Project Overview
This project analyzes the relationship between Bitcoin market sentiment (Fear & Greed Index) and trader performance using historical trading data from Hyperliquid. The goal is to identify profitable trading patterns and strategies based on market conditions.

##  Technical Stack
- **Python 3.8+**
- **Libraries**: Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn
- **Data**: 
  - Hyperliquid historical trades (211,224 records)
  - Bitcoin Fear & Greed Index (2,644 daily records)

##  Key Findings
### Market Sentiment Impact
| Sentiment       | Avg PnL | Win Rate | Trade Volume |
|-----------------|--------:|---------:|-------------:|
| Extreme Greed   | 65.08   | 46.3%    | 3,164 USD    |
| Greed           | 50.12   | 39.3%    | 5,537 USD    |
| Neutral         | 32.91   | 36.2%    | 4,846 USD    |

### Top Correlations
1. Trade Size ↔ Fees: 0.75
2. Trade Value ↔ PnL: 0.12
3. Sentiment ↔ PnL: 0.006 (weak)

##  Sample Visualizations
![Sentiment Distribution](data/outputs/sentiment_distribution.png) 
![Trader Clusters](data/outputs/cluster_analysis.png)

##  How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Place raw data in `data/raw/`
3. Execute the pipeline:
   ```bash
   python src/main.py
   ```

##  Outputs Generated
- `merged_data.csv` - Processed dataset (211,224 records)
- `trader_metrics.csv` - Performance by trader
- Visualizations (PNG)
- Statistical test results
- Summary report (`analysis_report.txt`)

##  Strategic Recommendations
1. **Increase positions** during "Extreme Greed" periods (65.08 avg PnL)
2. **Reduce exposure** during Neutral markets (32.91 avg PnL)
3. **Emulate Cluster 2 traders** (high win rate + optimal leverage)

##  Future Enhancements
- Incorporate on-chain data
- Build predictive models
- Real-time sentiment integration


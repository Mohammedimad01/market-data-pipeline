# Daily Market Data Pipeline

[![Daily Market Data Pipeline](https://github.com/USERNAME/market-data-pipeline/actions/workflows/daily_pipeline.yml/badge.svg)](https://github.com/USERNAME/market-data-pipeline/actions/workflows/daily_pipeline.yml)

A production-ready data engineering pipeline that automatically collects daily stock and cryptocurrency market data, cleans it, calculates analytics, generates charts, and updates this README dashboard using Python and GitHub Actions.

---

<!-- DASHBOARD_START -->

## 📅 Daily Market Dashboard

*Last Updated: 2026-08-08 01:10 UTC*

### Stocks

| Asset | Price | 24h Change | 7-Day MA |
|-------|-------|------------|----------|
| **AAPL** | $313.33 | +0.29% | $313.13 |
| **AMZN** | $274.48 | +0.82% | $269.70 |
| **GOOGL** | $354.30 | -0.96% | $359.35 |
| **MSFT** | $499.99 | +0.03% | $483.37 |
| **NVDA** | $223.96 | +2.27% | $210.93 |
| **TSLA** | $328.58 | +2.83% | $319.88 |

### Crypto

| Asset | Price | 24h Change | 7-Day MA |
|-------|-------|------------|----------|
| **BNB-USD** | $590.73 | -0.29% | $592.73 |
| **BTC-USD** | $64,881 | +0.89% | $64,168.88 |
| **ETH-USD** | $1,914 | +0.68% | $1,890.18 |
| **SOL-USD** | $73.65 | +1.43% | $73.57 |
| **XRP-USD** | $1.03 | -0.77% | $1.06 |

### 📈 Daily Market Movers

- **Top Gainer:** TSLA (+2.83%)
- **Top Loser:** GOOGL (-0.96%)

### 📉 Latest Charts

![Portfolio Summary](charts/portfolio_summary.png)

<div style='display: flex; gap: 10px;'>
<img src='charts/btc_price.png' width='45%'>
<img src='charts/aapl_price.png' width='45%'>
</div>

### 📊 Dataset Statistics

- **Historical Days Collected:** 18
- **Total Records:** 160
- **Pipeline Status:** Healthy 🟢

<!-- DASHBOARD_END -->

---

## 🏗️ Architecture & Project Structure

The pipeline is built using a modular Python architecture.

```text
market-data-pipeline/
├── data/                   # Raw and processed CSV datasets
├── charts/                 # Generated Matplotlib visualizations
├── src/                    # Core Python modules
│   ├── config.py           # Configuration and assets
│   ├── logger.py           # Standardized logging
│   ├── fetch.py            # API ingestion
│   ├── clean.py            # Data cleaning and validation (Pandas)
│   ├── analytics.py        # Moving averages and volatility
│   ├── charts.py           # Data visualization
│   └── update_readme.py    # Markdown dashboard generation
├── .github/workflows/      # GitHub Actions CI/CD automation
├── main.py                 # Orchestrator script
└── requirements.txt        # Python dependencies
```

## 🔄 Pipeline Flow

1. **GitHub Actions Trigger:** The workflow `.github/workflows/daily_pipeline.yml` runs every day at midnight UTC (or manually).
2. **Data Ingestion (`fetch.py`):** Downloads the latest OHLCV market data using a public API. Includes robust retries, timeouts, and error handling.
3. **Data Cleaning (`clean.py`):** Loads the raw JSON, formats timestamps, handles missing values, and appends the new data to historical CSVs (`data/stocks.csv`, `data/crypto.csv`) while preventing duplicates.
4. **Analytics (`analytics.py`):** Calculates 7-day and 30-day Moving Averages, Daily Returns, and Volatility using Pandas rolling windows.
5. **Visualization (`charts.py`):** Generates PNG charts using Matplotlib to visualize price history and portfolio summaries.
6. **Dashboard Update (`update_readme.py`):** Parses the generated analytics and dynamically rewrites the Dashboard section in this `README.md`.
7. **Automated Commit:** The GitHub Actions runner commits and pushes the updated data, charts, and README back to the repository if changes exist.

## 🚀 Installation & Running Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/USERNAME/market-data-pipeline.git
   cd market-data-pipeline
   ```

2. **Create a virtual environment (Optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the pipeline**
   ```bash
   python main.py
   ```

## ⚙️ Customization

You can easily track different assets by modifying the `STOCKS` and `CRYPTO` lists inside `src/config.py`. 

```python
STOCKS = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "TSLA", "META"]
CRYPTO = ["BTC-USD", "ETH-USD", "SOL-USD"]
```

## 🔮 Future Improvements
- [ ] Connect a PostgreSQL database or BigQuery for scalable storage.
- [ ] Add Email/Slack notifications for daily summaries or price alerts.
- [ ] Integrate a paid financial API (e.g., Alpha Vantage, Polygon) for higher frequency data.
- [ ] Implement data quality testing using Great Expectations.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

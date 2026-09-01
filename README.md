# Daily Market Data Pipeline

[![Daily Market Data Pipeline](https://github.com/USERNAME/market-data-pipeline/actions/workflows/daily_pipeline.yml/badge.svg)](https://github.com/USERNAME/market-data-pipeline/actions/workflows/daily_pipeline.yml)

A production-ready data engineering pipeline that automatically collects daily stock and cryptocurrency market data, cleans it, calculates analytics, generates charts, and updates this README dashboard using Python and GitHub Actions.

---

<!-- DASHBOARD_START -->

## 📅 Daily Market Dashboard

*Last Updated: 2026-09-01 03:09 UTC*

### Stocks

| Asset | Price | 24h Change | 7-Day MA |
|-------|-------|------------|----------|
| **AAPL** | $316.85 | -0.89% | $313.45 |
| **AMZN** | $259.77 | -2.50% | $260.64 |
| **GOOGL** | $339.35 | -2.09% | $344.06 |
| **MSFT** | $507.29 | -1.22% | $497.79 |
| **NVDA** | $220.78 | +1.48% | $216.03 |
| **TSLA** | $367.95 | +5.51% | $354.20 |

### Crypto

| Asset | Price | 24h Change | 7-Day MA |
|-------|-------|------------|----------|
| **BNB-USD** | $692.26 | +0.18% | $698.40 |
| **BTC-USD** | $78,417 | +0.93% | $78,703.74 |
| **ETH-USD** | $2,464 | +0.92% | $2,478.43 |
| **SOL-USD** | $103.28 | -0.83% | $101.10 |
| **XRP-USD** | $1.38 | -0.96% | $1.43 |

### 📈 Daily Market Movers

- **Top Gainer:** TSLA (+5.51%)
- **Top Loser:** AMZN (-2.50%)

### 📉 Latest Charts

![Portfolio Summary](charts/portfolio_summary.png)

<div style='display: flex; gap: 10px;'>
<img src='charts/btc_price.png' width='45%'>
<img src='charts/aapl_price.png' width='45%'>
</div>

### 📊 Dataset Statistics

- **Historical Days Collected:** 38
- **Total Records:** 336
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

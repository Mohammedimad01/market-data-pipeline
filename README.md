# Daily Market Data Pipeline

[![Daily Market Data Pipeline](https://github.com/USERNAME/market-data-pipeline/actions/workflows/daily_pipeline.yml/badge.svg)](https://github.com/USERNAME/market-data-pipeline/actions/workflows/daily_pipeline.yml)

A production-ready data engineering pipeline that automatically collects daily stock and cryptocurrency market data, cleans it, calculates analytics, generates charts, and updates this README dashboard using Python and GitHub Actions.

---

<!-- DASHBOARD_START -->

## 📅 Daily Market Dashboard

*Last Updated: 2026-07-21 01:59 UTC*

### Stocks

| Asset | Price | 24h Change | 7-Day MA |
|-------|-------|------------|----------|
| **AAPL** | $326.59 | nan% | $326.59 |
| **AMZN** | $249.99 | nan% | $249.99 |
| **GOOGL** | $351.99 | nan% | $351.99 |
| **MSFT** | $402.29 | nan% | $402.29 |
| **NVDA** | $203.28 | nan% | $203.28 |
| **TSLA** | $369.57 | nan% | $369.57 |

### Crypto

| Asset | Price | 24h Change | 7-Day MA |
|-------|-------|------------|----------|
| **BNB-USD** | $571.68 | nan% | $571.68 |
| **BTC-USD** | $65,194 | nan% | $65,193.84 |
| **ETH-USD** | $1,906 | nan% | $1,906.05 |
| **SOL-USD** | $77.78 | nan% | $77.78 |
| **XRP-USD** | $1.11 | nan% | $1.11 |

### 📉 Latest Charts

![Portfolio Summary](charts/portfolio_summary.png)

<div style='display: flex; gap: 10px;'>
<img src='charts/btc_price.png' width='45%'>
<img src='charts/aapl_price.png' width='45%'>
</div>

### 📊 Dataset Statistics

- **Historical Days Collected:** 2
- **Total Records:** 11
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

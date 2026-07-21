import os
import pathlib

# Project structure
BASE_DIR = pathlib.Path(__file__).parent.parent.resolve()
DATA_DIR = BASE_DIR / "data"
CHARTS_DIR = BASE_DIR / "charts"

# Ensure directories exist (for local execution)
DATA_DIR.mkdir(parents=True, exist_ok=True)
CHARTS_DIR.mkdir(parents=True, exist_ok=True)

# File paths
STOCKS_CSV = DATA_DIR / "stocks.csv"
CRYPTO_CSV = DATA_DIR / "crypto.csv"
LATEST_JSON = DATA_DIR / "latest.json"

# Assets to track
STOCKS = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "TSLA"]
CRYPTO = ["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "XRP-USD"] # Yahoo Finance format

# API settings
# We use Yahoo Finance's unofficial public chart API endpoint which requires no auth.
API_URL_TEMPLATE = "https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=1d&interval=1d"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Retry settings
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2
TIMEOUT_SECONDS = 10

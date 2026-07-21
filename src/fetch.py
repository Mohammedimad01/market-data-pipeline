import json
import time
import requests
from typing import Dict, Any, List

from src.config import API_URL_TEMPLATE, USER_AGENT, LATEST_JSON, MAX_RETRIES, RETRY_DELAY_SECONDS, TIMEOUT_SECONDS, STOCKS, CRYPTO
from src.logger import get_logger

logger = get_logger("fetch")

def fetch_ticker_data(ticker: str) -> Dict[str, Any]:
    """
    Fetches the latest daily chart data for a given ticker from Yahoo Finance.
    Handles retries, timeouts, and basic validation.
    """
    url = API_URL_TEMPLATE.format(ticker=ticker)
    headers = {"User-Agent": USER_AGENT}
    
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, headers=headers, timeout=TIMEOUT_SECONDS)
            response.raise_for_status()
            
            data = response.json()
            
            # Basic validation to ensure data exists
            if not data.get("chart", {}).get("result"):
                logger.warning(f"No result found for {ticker}")
                return {}
                
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Attempt {attempt}/{MAX_RETRIES} failed for {ticker}: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY_SECONDS)
            else:
                logger.error(f"Failed to fetch data for {ticker} after {MAX_RETRIES} attempts.")
                return {}
        except ValueError as e:
            logger.error(f"JSON decode error for {ticker}: {e}")
            return {}

def fetch_all_data() -> None:
    """
    Iterates over all defined assets, fetches their data, and saves to latest.json.
    """
    all_data = {
        "stocks": {},
        "crypto": {}
    }
    
    logger.info("Starting to download market data...")
    
    # Fetch Stocks
    for ticker in STOCKS:
        logger.info(f"Fetching stock: {ticker}")
        data = fetch_ticker_data(ticker)
        if data:
            all_data["stocks"][ticker] = data
            
    # Fetch Crypto
    for ticker in CRYPTO:
        logger.info(f"Fetching crypto: {ticker}")
        data = fetch_ticker_data(ticker)
        if data:
            all_data["crypto"][ticker] = data
            
    # Save to JSON
    with open(LATEST_JSON, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=4)
        
    logger.info(f"Successfully saved raw data to {LATEST_JSON}")

if __name__ == "__main__":
    fetch_all_data()

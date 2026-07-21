import json
import pandas as pd
from typing import Dict, Any

from src.config import LATEST_JSON, STOCKS_CSV, CRYPTO_CSV
from src.logger import get_logger

logger = get_logger("clean")

def extract_ohlcv(data: Dict[str, Any], symbol: str) -> pd.DataFrame:
    """
    Extracts timestamp and OHLCV from the Yahoo Finance JSON response.
    Returns a Pandas DataFrame.
    """
    try:
        result = data["chart"]["result"][0]
        timestamps = result["timestamp"]
        quote = result["indicators"]["quote"][0]
        
        # In case of missing data arrays, we return empty DataFrame
        if not timestamps or not quote:
            return pd.DataFrame()
            
        df = pd.DataFrame({
            "Date": pd.to_datetime(timestamps, unit="s", utc=True).strftime('%Y-%m-%d'),
            "Timestamp": timestamps,
            "Symbol": symbol,
            "Open": quote.get("open", []),
            "High": quote.get("high", []),
            "Low": quote.get("low", []),
            "Close": quote.get("close", []),
            "Volume": quote.get("volume", [])
        })
        
        # Drop rows with NaN in critical columns
        df.dropna(subset=["Open", "High", "Low", "Close"], inplace=True)
        return df
        
    except KeyError as e:
        logger.error(f"Missing expected key in JSON structure for {symbol}: {e}")
        return pd.DataFrame()

def process_and_append(category_data: Dict[str, Any], csv_path: str) -> None:
    """
    Processes all symbols in a category, appends to the master CSV, 
    and removes duplicates keeping the latest.
    """
    new_rows = []
    
    for symbol, data in category_data.items():
        df = extract_ohlcv(data, symbol)
        if not df.empty:
            new_rows.append(df)
            
    if not new_rows:
        logger.warning(f"No valid new data found to append to {csv_path}")
        return
        
    new_df = pd.concat(new_rows, ignore_index=True)
    
    # Load existing CSV if it exists
    try:
        if csv_path.exists():
            existing_df = pd.read_csv(csv_path)
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        else:
            combined_df = new_df
            
        # Remove duplicates based on Symbol and Date, keeping the last (newest) entry
        combined_df.drop_duplicates(subset=["Symbol", "Date"], keep="last", inplace=True)
        
        # Sort by Date and Symbol for consistency
        combined_df.sort_values(by=["Date", "Symbol"], inplace=True)
        
        # Save back to CSV
        combined_df.to_csv(csv_path, index=False)
        logger.info(f"Successfully appended and cleaned data in {csv_path.name}")
        
    except Exception as e:
        logger.error(f"Error processing CSV {csv_path}: {e}")

def clean_data() -> None:
    """
    Reads the raw latest.json file and processes stocks and crypto data.
    """
    logger.info("Cleaning Dataset...")
    
    if not LATEST_JSON.exists():
        logger.error(f"Raw data file not found: {LATEST_JSON}")
        return
        
    with open(LATEST_JSON, 'r', encoding='utf-8') as f:
        try:
            all_data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding {LATEST_JSON}: {e}")
            return

    if "stocks" in all_data:
        process_and_append(all_data["stocks"], STOCKS_CSV)
        
    if "crypto" in all_data:
        process_and_append(all_data["crypto"], CRYPTO_CSV)
        
if __name__ == "__main__":
    clean_data()

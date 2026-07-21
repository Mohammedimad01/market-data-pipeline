import pandas as pd
import numpy as np
from typing import Dict

from src.config import STOCKS_CSV, CRYPTO_CSV
from src.logger import get_logger

logger = get_logger("analytics")

def calculate_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates technical and statistical metrics for a single symbol's historical data.
    Assumes df is sorted by Date.
    """
    # Ensure Date is datetime type
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Moving Averages
    df['MA_7'] = df['Close'].rolling(window=7, min_periods=1).mean()
    df['MA_30'] = df['Close'].rolling(window=30, min_periods=1).mean()
    
    # Returns
    df['Daily_Return'] = df['Close'].pct_change()
    df['Percentage_Change'] = df['Daily_Return'] * 100
    
    # Volatility (30-day standard deviation of daily returns)
    df['Volatility_30'] = df['Daily_Return'].rolling(window=30, min_periods=1).std() * np.sqrt(365) # Annualized
    
    # Highs and Lows (30-day)
    df['Highest_30'] = df['High'].rolling(window=30, min_periods=1).max()
    df['Lowest_30'] = df['Low'].rolling(window=30, min_periods=1).min()
    
    # Average Price
    df['Average_Price'] = df['Close'].expanding().mean()
    
    return df

def process_file(csv_path: str) -> pd.DataFrame:
    """
    Reads a CSV, groups by Symbol, applies metrics, and returns the full DataFrame.
    """
    if not csv_path.exists():
        logger.warning(f"File not found for analytics: {csv_path}")
        return pd.DataFrame()
        
    df = pd.read_csv(csv_path)
    
    if df.empty:
        return df
        
    logger.info(f"Generating analytics for {csv_path.name}")
    
    # Apply calculations per symbol
    processed_dfs = []
    for symbol, group in df.groupby('Symbol'):
        # Ensure it's sorted by Date before rolling windows
        group = group.sort_values(by='Date').copy()
        processed_group = calculate_metrics(group)
        processed_dfs.append(processed_group)
        
    final_df = pd.concat(processed_dfs, ignore_index=True)
    
    # Overwrite CSV with enriched data
    final_df.to_csv(csv_path, index=False)
    return final_df

def generate_analytics() -> Dict[str, pd.DataFrame]:
    """
    Main entry point for analytics. Processes both stocks and crypto.
    Returns the enriched dataframes.
    """
    logger.info("Starting analytics generation...")
    
    results = {}
    
    stocks_df = process_file(STOCKS_CSV)
    if not stocks_df.empty:
        results['stocks'] = stocks_df
        
    crypto_df = process_file(CRYPTO_CSV)
    if not crypto_df.empty:
        results['crypto'] = crypto_df
        
    return results

if __name__ == "__main__":
    generate_analytics()

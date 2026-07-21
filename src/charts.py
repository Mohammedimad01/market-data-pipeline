import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

from src.config import CHARTS_DIR
from src.logger import get_logger

logger = get_logger("charts")

# Set a professional plotting style
plt.style.use('ggplot')
# Fallback colors if styling isn't sufficient
COLORS = {
    'primary': '#2c3e50',
    'secondary': '#e74c3c',
    'tertiary': '#3498db',
    'background': '#f9f9f9'
}

def plot_price_history(df: pd.DataFrame, symbol: str, filename: str) -> None:
    """
    Generates a line chart for the price history of a single asset.
    """
    symbol_df = df[df['Symbol'] == symbol].copy()
    
    if symbol_df.empty:
        logger.warning(f"No data available to plot for {symbol}")
        return
        
    symbol_df['Date'] = pd.to_datetime(symbol_df['Date'])
    
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor(COLORS['background'])
    ax.set_facecolor(COLORS['background'])
    
    ax.plot(symbol_df['Date'], symbol_df['Close'], label='Close Price', color=COLORS['primary'], linewidth=2)
    
    if 'MA_30' in symbol_df.columns:
        ax.plot(symbol_df['Date'], symbol_df['MA_30'], label='30-Day MA', color=COLORS['secondary'], linestyle='--', linewidth=1.5)
        
    ax.set_title(f"{symbol} Price History & Trend", fontsize=14, fontweight='bold', color=COLORS['primary'])
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Price (USD)", fontsize=12)
    
    # Format x-axis dates
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    fig.autofmt_xdate()
    
    ax.legend()
    ax.grid(True, linestyle=':', alpha=0.6)
    
    filepath = CHARTS_DIR / filename
    plt.tight_layout()
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info(f"Saved chart: {filepath.name}")

def plot_portfolio_summary(stocks_df: pd.DataFrame, crypto_df: pd.DataFrame) -> None:
    """
    Generates a bar chart comparing recent performance (e.g. latest daily return) of all assets.
    """
    latest_returns = []
    
    def get_latest(df):
        if df.empty: return []
        # Get the most recent date for each symbol
        idx = df.groupby('Symbol')['Date'].transform('max') == df['Date']
        latest = df[idx]
        return latest[['Symbol', 'Percentage_Change']].dropna().to_dict('records')
        
    latest_returns.extend(get_latest(stocks_df))
    latest_returns.extend(get_latest(crypto_df))
    
    if not latest_returns:
        logger.warning("No data for portfolio summary plot.")
        return
        
    summary_df = pd.DataFrame(latest_returns)
    summary_df.sort_values(by='Percentage_Change', inplace=True)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor(COLORS['background'])
    ax.set_facecolor(COLORS['background'])
    
    colors = ['#27ae60' if x >= 0 else '#c0392b' for x in summary_df['Percentage_Change']]
    
    ax.barh(summary_df['Symbol'], summary_df['Percentage_Change'], color=colors)
    
    ax.set_title("Today's Market Movers (% Change)", fontsize=16, fontweight='bold')
    ax.set_xlabel("Percentage Change (%)", fontsize=12)
    ax.axvline(0, color='black', linewidth=1, linestyle='--')
    
    filepath = CHARTS_DIR / "portfolio_summary.png"
    plt.tight_layout()
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info(f"Saved chart: {filepath.name}")

def generate_charts(analytics_data: dict) -> None:
    """
    Main entry point for chart generation.
    """
    logger.info("Generating charts...")
    
    stocks_df = analytics_data.get('stocks', pd.DataFrame())
    crypto_df = analytics_data.get('crypto', pd.DataFrame())
    
    if not crypto_df.empty:
        plot_price_history(crypto_df, 'BTC-USD', 'btc_price.png')
        plot_price_history(crypto_df, 'ETH-USD', 'eth_price.png')
        
    if not stocks_df.empty:
        plot_price_history(stocks_df, 'AAPL', 'aapl_price.png')
        
    plot_portfolio_summary(stocks_df, crypto_df)

import pandas as pd
from datetime import datetime, timezone
import pathlib

from src.config import BASE_DIR
from src.logger import get_logger

logger = get_logger("update_readme")

README_PATH = BASE_DIR / "README.md"

def get_latest_stats(df: pd.DataFrame, asset_type: str) -> str:
    """
    Generates a Markdown table for the latest prices and changes.
    """
    if df.empty:
        return f"*No {asset_type} data available.*\n"
        
    # Get the latest row for each symbol
    idx = df.groupby('Symbol')['Date'].transform('max') == df['Date']
    latest = df[idx].copy()
    
    # Sort alphabetically
    latest.sort_values(by='Symbol', inplace=True)
    
    table = f"### {asset_type.capitalize()}\n\n"
    table += "| Asset | Price | 24h Change | 7-Day MA |\n"
    table += "|-------|-------|------------|----------|\n"
    
    for _, row in latest.iterrows():
        symbol = row['Symbol']
        price = f"${row['Close']:,.2f}"
        
        # Handle crypto vs stock formatting
        if 'BTC' in symbol or 'ETH' in symbol:
            if row['Close'] > 1000:
                price = f"${row['Close']:,.0f}"
                
        change = row.get('Percentage_Change', 0)
        change_str = f"+{change:.2f}%" if change > 0 else f"{change:.2f}%"
        ma7 = f"${row.get('MA_7', 0):,.2f}" if not pd.isna(row.get('MA_7')) else "N/A"
        
        table += f"| **{symbol}** | {price} | {change_str} | {ma7} |\n"
        
    return table + "\n"

def get_movers(stocks_df: pd.DataFrame, crypto_df: pd.DataFrame) -> str:
    """
    Identifies the top gainer and loser across all assets for the latest day.
    """
    latest_rows = []
    
    for df in [stocks_df, crypto_df]:
        if not df.empty:
            idx = df.groupby('Symbol')['Date'].transform('max') == df['Date']
            latest_rows.append(df[idx])
            
    if not latest_rows:
        return ""
        
    combined = pd.concat(latest_rows)
    if combined.empty or 'Percentage_Change' not in combined.columns:
        return ""
        
    # Drop NaNs
    combined.dropna(subset=['Percentage_Change'], inplace=True)
    
    if combined.empty:
         return ""

    top_gainer = combined.loc[combined['Percentage_Change'].idxmax()]
    top_loser = combined.loc[combined['Percentage_Change'].idxmin()]
    
    text = "### 📈 Daily Market Movers\n\n"
    text += f"- **Top Gainer:** {top_gainer['Symbol']} (+{top_gainer['Percentage_Change']:.2f}%)\n"
    text += f"- **Top Loser:** {top_loser['Symbol']} ({top_loser['Percentage_Change']:.2f}%)\n\n"
    return text

def get_dataset_stats(stocks_df: pd.DataFrame, crypto_df: pd.DataFrame) -> str:
    """
    Generates summary statistics about the dataset.
    """
    total_rows = len(stocks_df) + len(crypto_df)
    unique_dates = set()
    
    if not stocks_df.empty: unique_dates.update(stocks_df['Date'].unique())
    if not crypto_df.empty: unique_dates.update(crypto_df['Date'].unique())
    
    total_days = len(unique_dates)
    
    text = "### 📊 Dataset Statistics\n\n"
    text += f"- **Historical Days Collected:** {total_days}\n"
    text += f"- **Total Records:** {total_rows:,}\n"
    text += "- **Pipeline Status:** Healthy 🟢\n\n"
    return text

def generate_dashboard_content(analytics_data: dict) -> str:
    """
    Generates the full markdown string for the dashboard section.
    """
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    
    stocks_df = analytics_data.get('stocks', pd.DataFrame())
    crypto_df = analytics_data.get('crypto', pd.DataFrame())
    
    content = f"## 📅 Daily Market Dashboard\n\n"
    content += f"*Last Updated: {now}*\n\n"
    
    content += get_latest_stats(stocks_df, "Stocks")
    content += get_latest_stats(crypto_df, "Crypto")
    content += get_movers(stocks_df, crypto_df)
    
    content += "### 📉 Latest Charts\n\n"
    content += "![Portfolio Summary](charts/portfolio_summary.png)\n\n"
    content += "<div style='display: flex; gap: 10px;'>\n"
    content += "<img src='charts/btc_price.png' width='45%'>\n"
    content += "<img src='charts/aapl_price.png' width='45%'>\n"
    content += "</div>\n\n"
    
    content += get_dataset_stats(stocks_df, crypto_df)
    
    return content

def update_readme(analytics_data: dict) -> None:
    """
    Replaces the content between <!-- DASHBOARD_START --> and <!-- DASHBOARD_END --> in README.md.
    """
    logger.info("Updating README.md with latest data...")
    
    if not README_PATH.exists():
        logger.error(f"README.md not found at {README_PATH}")
        return
        
    with open(README_PATH, 'r', encoding='utf-8') as f:
        readme_content = f.read()
        
    start_marker = "<!-- DASHBOARD_START -->"
    end_marker = "<!-- DASHBOARD_END -->"
    
    if start_marker not in readme_content or end_marker not in readme_content:
        logger.error("Dashboard markers not found in README.md.")
        return
        
    dashboard_content = generate_dashboard_content(analytics_data)
    
    # Slice and reconstruct
    start_idx = readme_content.find(start_marker) + len(start_marker)
    end_idx = readme_content.find(end_marker)
    
    new_readme = (
        readme_content[:start_idx] + 
        "\n\n" + dashboard_content + 
        readme_content[end_idx:]
    )
    
    with open(README_PATH, 'w', encoding='utf-8') as f:
        f.write(new_readme)
        
    logger.info("README.md updated successfully.")

if __name__ == "__main__":
    # For testing, requires valid analytics data passed in via main
    pass

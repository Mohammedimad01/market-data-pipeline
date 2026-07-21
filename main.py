import sys
from src.logger import get_logger
from src.fetch import fetch_all_data
from src.clean import clean_data
from src.analytics import generate_analytics
from src.charts import generate_charts
from src.update_readme import update_readme

logger = get_logger("main")

def run_pipeline():
    """
    Orchestrates the entire daily market data pipeline.
    """
    logger.info("="*50)
    logger.info("Starting Daily Market Data Pipeline")
    logger.info("="*50)
    
    try:
        # Step 1: Fetch raw data
        logger.info("\n--- STEP 1: Fetching Market Data ---")
        fetch_all_data()
        
        # Step 2 & 3: Clean and append historical data
        logger.info("\n--- STEP 2 & 3: Cleaning & Appending Dataset ---")
        clean_data()
        
        # Step 4: Generate Analytics
        logger.info("\n--- STEP 4: Generating Analytics ---")
        analytics_data = generate_analytics()
        
        if not analytics_data:
            logger.error("No analytics data generated. Pipeline halting.")
            sys.exit(1)
            
        # Step 5: Generate Charts
        logger.info("\n--- STEP 5: Generating Charts ---")
        generate_charts(analytics_data)
        
        # Step 6: Update README Dashboard
        logger.info("\n--- STEP 6: Updating README.md ---")
        update_readme(analytics_data)
        
        logger.info("="*50)
        logger.info("Pipeline Completed Successfully")
        logger.info("="*50)
        
    except Exception as e:
        logger.error(f"Pipeline failed with an unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_pipeline()

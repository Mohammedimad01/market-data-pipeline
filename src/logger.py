import logging
import sys

def get_logger(name: str) -> logging.Logger:
    """
    Creates and configures a professional logger.
    Outputs to standard out with formatting.
    """
    logger = logging.getLogger(name)
    
    # Only configure if it doesn't already have handlers
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger

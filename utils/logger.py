import logging
import sys
from config.settings import LOG_FILE, LOG_FORMAT, LOG_LEVEL

def setup_logger(name: str) -> logging.Logger:
    """
    Initializes and returns a customized logger.
    
    Args:
        name (str): The name of the module invoking the logger.
        
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    
    # Prevent duplicate logs if logger is called multiple times
    if logger.hasHandlers():
        return logger

    logger.setLevel(LOG_LEVEL)

    # Create file handler
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(LOG_LEVEL)

    # Create console handler (Standard Output)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.ERROR) # Only print critical errors to standard console directly

    # Create formatter and add it to the handlers
    formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

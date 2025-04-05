#!/usr/bin/env python3
import logging
import os
import os
import sys

# Dynamically add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def setup_logger(name: str = __name__, log_file: str = "app.log", level=logging.INFO) -> logging.Logger:
    """
    Set up a logger with a specified name, output file, and logging level.
    
    Logs are written both to the console and to the specified log file.
    
    Parameters:
      name (str): The name of the logger.
      log_file (str): The log file path.
      level: Logging level (e.g., logging.INFO).
      
    Returns:
      logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False  # Prevent log messages from being propagated to the root logger
    
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)
    
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger

if __name__ == "__main__":
    logger = setup_logger("test_logger", "test_app.log")
    logger.info("This is an info message.")
    logger.debug("This is a debug message.")
    logger.error("This is an error message.")

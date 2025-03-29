# utils/decorators.py

import time
import logging
from functools import wraps

logger = logging.getLogger(__name__)

def timeit(func):
    """
    Decorator that logs the execution time of a function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        logger.info(f"{func.__name__} took {duration:.2f} seconds")
        return result
    return wrapper

def log_exceptions(func):
    """
    Decorator that logs any exceptions raised in the wrapped function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(f"Exception in {func.__name__}: {e}")
            raise
    return wrapper

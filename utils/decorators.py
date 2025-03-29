#!/usr/bin/env python3
import time
import functools

def timeit(func):
    """
    Decorator to measure the execution time of a function.
    """
    @functools.wraps(func)
    def wrapper_timeit(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start_time
        print(f"Function '{func.__name__}' executed in {elapsed:.4f} seconds.")
        return result
    return wrapper_timeit

def retry(max_retries=3, delay=1, exceptions=(Exception,)):
    """
    Decorator to retry a function if specified exceptions are raised.

    Parameters:
      max_retries (int): Maximum number of retry attempts.
      delay (int or float): Delay in seconds between retries.
      exceptions (tuple): Tuple of exception classes to catch.
    """
    def decorator_retry(func):
        @functools.wraps(func)
        def wrapper_retry(*args, **kwargs):
            attempt = 0
            while attempt < max_retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    print(f"Attempt {attempt}/{max_retries} for '{func.__name__}' failed with error: {e}. Retrying in {delay} seconds...")
                    time.sleep(delay)
            raise Exception(f"Function '{func.__name__}' failed after {max_retries} attempts.")
        return wrapper_retry
    return decorator_retry

if __name__ == "__main__":
    @timeit
    def example_sleep(n):
        time.sleep(n)
        return n

    @retry(max_retries=5, delay=0.5, exceptions=(ValueError,))
    def example_retry(n):
        if n < 3:
            raise ValueError("n is less than 3")
        return n

    print("Testing timeit decorator:")
    print(example_sleep(1))

    print("Testing retry decorator:")
    try:
        print(example_retry(2))
    except Exception as e:
        print(e)
    print(example_retry(3))

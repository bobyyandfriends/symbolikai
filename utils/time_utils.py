# utils/time_utils.py

from datetime import datetime, timedelta
import pandas as pd

def parse_timestamp(ts: str) -> pd.Timestamp:
    """
    Convert string to pandas Timestamp.
    Accepts formats like: "2024-01-01 13:30", "2024-01-01", etc.
    """
    try:
        return pd.to_datetime(ts)
    except Exception:
        raise ValueError(f"Unrecognized timestamp format: {ts}")


def get_market_open_close(date: str) -> tuple[pd.Timestamp, pd.Timestamp]:
    """
    Given a date string, return the market open/close timestamps for that day.
    """
    base_date = pd.to_datetime(date)
    open_time = base_date.replace(hour=9, minute=30)
    close_time = base_date.replace(hour=16, minute=0)
    return open_time, close_time


def get_next_trading_day(date: str, calendar: list[str] = None) -> str:
    """
    Return the next valid trading day after the given date.
    Optionally pass a list of valid trading dates (calendar).
    """
    d = pd.to_datetime(date)
    while True:
        d += timedelta(days=1)
        if calendar:
            if d.strftime("%Y-%m-%d") in calendar:
                return d.strftime("%Y-%m-%d")
        elif d.weekday() < 5:  # Mon-Fri
            return d.strftime("%Y-%m-%d")


def filter_market_hours(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filters a minute-level DataFrame to only include regular market hours (9:30 AM to 4:00 PM).
    Assumes the index is datetime.
    """
    return df.between_time("09:30", "16:00")

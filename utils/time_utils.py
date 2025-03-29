#!/usr/bin/env python3
import datetime
from typing import Union

def to_datetime(dt: Union[str, datetime.datetime]) -> datetime.datetime:
    """
    Convert a string or datetime object to a datetime object.
    
    Parameters:
      dt: A string in ISO format (or other common formats) or a datetime object.
      
    Returns:
      A datetime.datetime object.
      
    Raises:
      ValueError if the input string cannot be parsed.
    """
    if isinstance(dt, datetime.datetime):
        return dt
    try:
        return datetime.datetime.fromisoformat(dt)
    except Exception as e:
        raise ValueError(f"Unable to parse datetime from: {dt}") from e

def round_datetime(dt: datetime.datetime, round_to: int = 60) -> datetime.datetime:
    """
    Round a datetime object to the nearest multiple of a given number of seconds.
    
    Parameters:
      dt: The datetime object to round.
      round_to: The number of seconds to round to (default is 60 seconds, i.e. nearest minute).
      
    Returns:
      A new datetime object rounded to the nearest multiple of round_to seconds.
    """
    # Calculate seconds since midnight
    midnight = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    seconds_since_midnight = (dt - midnight).total_seconds()
    # Round the seconds
    rounding = int((seconds_since_midnight + round_to / 2) // round_to * round_to)
    return midnight + datetime.timedelta(seconds=rounding)

def get_time_difference(start: datetime.datetime, end: datetime.datetime) -> float:
    """
    Calculate the difference between two datetime objects in seconds.
    
    Parameters:
      start: The start datetime.
      end: The end datetime.
      
    Returns:
      The time difference in seconds as a float.
    """
    return (end - start).total_seconds()

if __name__ == "__main__":
    # Example usage:
    dt_str = "2023-03-29T12:34:56"
    dt_obj = to_datetime(dt_str)
    print("Parsed datetime:", dt_obj)
    
    rounded_dt = round_datetime(dt_obj, round_to=60)
    print("Rounded datetime (nearest minute):", rounded_dt)
    
    diff_seconds = get_time_difference(dt_obj, rounded_dt)
    print("Difference in seconds:", diff_seconds)

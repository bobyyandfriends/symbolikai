#!/usr/bin/env python3
import os
import pandas as pd

def get_price_path(symbol: str, timeframe: str) -> str:
    """
    Construct the file path for the given symbol and timeframe.
    Price data is expected to be stored in a subfolder 'price_data' inside this directory.
    Naming convention: SYMBOL_timeframe.csv (e.g., AAPL_daily.csv).
    """
    base_dir = os.path.join(os.path.dirname(__file__), 'price_data')
    filename = f"{symbol}_{timeframe}.csv"
    return os.path.join(base_dir, filename)

def load_price_data(symbol: str, timeframe: str = 'daily') -> pd.DataFrame:
    """
    Load OHLCV price data for a given symbol and timeframe from a CSV file.
    The CSV should have columns: datetime, open, high, low, close, volume.
    The datetime column is parsed as dates, and the DataFrame is sorted by datetime.
    """
    file_path = get_price_path(symbol, timeframe)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Price data file not found: {file_path}")
    
    df = pd.read_csv(file_path, parse_dates=['datetime'])
    df.sort_values('datetime', inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

def resample_price_data(df: pd.DataFrame, new_timeframe: str) -> pd.DataFrame:
    """
    Resample price data to a new timeframe.
    new_timeframe should be a valid pandas offset alias (e.g., 'D' for daily, '240min' for 4-hour bars).
    Aggregates OHLCV data appropriately.
    """
    df = df.copy()
    df.set_index('datetime', inplace=True)
    ohlc_dict = {
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }
    resampled_df = df.resample(new_timeframe).apply(ohlc_dict).dropna()
    resampled_df.reset_index(inplace=True)
    return resampled_df

if __name__ == "__main__":
    symbol = "AAPL"
    timeframe = "daily"
    try:
        data = load_price_data(symbol, timeframe)
        print("Original data:")
        print(data.head())
        resampled = resample_price_data(data, '240min')
        print("\nResampled data:")
        print(resampled.head())
    except FileNotFoundError as err:
        print(err)

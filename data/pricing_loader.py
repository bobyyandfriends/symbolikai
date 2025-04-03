#!/usr/bin/env python3
import os
import pandas as pd

def get_price_path(symbol: str, timeframe: str) -> str:
    """
    Automatically use the correct folder based on timeframe.
    For example:
        - 'daily' → data/daily_data/
        - '240min' → data/240min_data/
    """
    # Get the absolute path to the base 'data' folder
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    folder_name = f"{timeframe}_data"  # e.g., "daily_data", "240min_data"
    filename = f"{symbol.upper()}_{timeframe}.csv"
    return os.path.join(data_dir, folder_name, filename)


def load_price_data(symbol: str, timeframe: str = 'daily') -> pd.DataFrame:
    """
    Load OHLCV from a CSV with columns 'timestamp','open','high','low','close','volume'.
    Parse 'timestamp' as datetime, sort it, and return.
    """
    fpath = get_price_path(symbol, timeframe)
    if not os.path.exists(fpath):
        raise FileNotFoundError(f"[pricing_loader] Not found: {fpath}")

    df = pd.read_csv(fpath)
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df.dropna(subset=['timestamp'], inplace=True)
    df.sort_values('timestamp', inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

def resample_price_data(df: pd.DataFrame, new_timeframe: str) -> pd.DataFrame:
    """
    Resample data to a new timeframe. 'timestamp' => index, then apply typical OHLC aggregator.
    e.g. new_timeframe = 'D' or '240min', etc.
    """
    df = df.copy()
    df.set_index('timestamp', inplace=True)
    ohlc_dict = {
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }
    # dropna ensures we discard any partial data
    resampled_df = df.resample(new_timeframe).apply(ohlc_dict).dropna()
    resampled_df.reset_index(inplace=True)
    return resampled_df

if __name__ == "__main__":
    # Quick test
    symbol = "AAPL"
    timeframe = "daily"
    try:
        data = load_price_data(symbol, timeframe)
        print("[pricing_loader] Loaded data sample:")
        print(data.head())
    except FileNotFoundError as e:
        print(e)

# data/pricing_loader.py

import os
import pandas as pd
from data.data_store import load_df_csv

BASE_PATH = os.path.join("data", "minute")

def get_price_path(symbol: str, timeframe: str) -> str:
    """
    Returns file path for the given symbol and timeframe.
    Currently supports only 'minute' data.
    """
    filename = f"{symbol.upper()}.csv"
    return os.path.join(BASE_PATH, filename)

def load_price_data(symbol: str, timeframe: str = "minute") -> pd.DataFrame:
    """
    Loads OHLCV price data for a given symbol.
    """
    path = get_price_path(symbol, timeframe)
    df = load_df_csv(path)

    # Ensure proper format
    df["symbol"] = df["symbol"].astype(str)
    df["datetime"] = pd.to_datetime(df["datetime"])
    df = df.sort_values("datetime").reset_index(drop=True)
    return df

def resample_price_data(df: pd.DataFrame, timeframe: str) -> pd.DataFrame:
    """
    Optional: Resamples 1-min data into other timeframes (e.g., 'daily', '240min').
    """
    df = df.set_index("datetime")
    rule = {"daily": "1D", "240": "240min"}.get(timeframe.lower())
    if not rule:
        raise ValueError(f"Unsupported resample timeframe: {timeframe}")

    ohlc = {
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }

    resampled = df.resample(rule).apply(ohlc).dropna().reset_index()
    resampled["symbol"] = df["symbol"].iloc[0]
    return resampled

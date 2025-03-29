#!/usr/bin/env python3
import pandas as pd
import pandas_ta as ta

def add_ta_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds technical analysis indicators to price data.
    The indicators include:
      - RSI (14-period)
      - Momentum (10-period)
      - ATR (14-period)
      - Bollinger Bands (20-period): upper, middle, lower bands
      - Keltner Channel: using a 20-period calculation (KCLe)
    Additionally, it creates binary columns indicating whether the close price
    is above the upper Bollinger Band or below the lower Bollinger Band.
    
    Parameters:
      df: DataFrame containing at least the columns 'high', 'low', 'close'
      
    Returns:
      A new DataFrame with additional columns for the technical indicators.
    """
    df = df.copy()
    
    df["rsi"] = ta.rsi(df["close"], length=14)
    df["mom"] = ta.mom(df["close"], length=10)
    df["atr"] = ta.atr(df["high"], df["low"], df["close"], length=14)
    
    # Bollinger Bands: The ta.bbands function returns a DataFrame;
    # we extract the upper, middle, and lower bands.
    bbands = ta.bbands(df["close"], length=20)
    df["bb_upper"] = bbands["BBU_20_2.0"]
    df["bb_middle"] = bbands["BBM_20_2.0"]
    df["bb_lower"] = bbands["BBL_20_2.0"]
    
    # Keltner Channel: Using the Keltner Channel lower band as an example indicator.
    # Depending on the library version, ta.kc returns a DataFrame; adjust key names if needed.
    kc = ta.kc(df["high"], df["low"], df["close"], length=20)
    # Here we assume 'KCLe_20_2.0' is available (the lower band).
    df["keltner"] = kc["KCLe_20_2.0"]
    
    # Create binary features for price relation to Bollinger Bands.
    df["price_above_bbands"] = (df["close"] > df["bb_upper"]).astype(int)
    df["price_below_bbands"] = (df["close"] < df["bb_lower"]).astype(int)
    
    return df

def merge_signals(price_df: pd.DataFrame, signal_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge signal timestamps with the engineered features from price data.
    This function renames the signal date column to 'timestamp' if necessary,
    resets the index of the price data, and performs an asof merge to align
    each signal with the most recent available price data.
    
    Parameters:
      price_df: DataFrame of price data with a 'timestamp' column.
      signal_df: DataFrame of signals, with a column named 'date' or 'timestamp'.
    
    Returns:
      A merged DataFrame with signals and corresponding technical features.
    """
    signal_df = signal_df.copy()
    # Rename column if necessary (from 'date' to 'timestamp')
    if "date" in signal_df.columns and "timestamp" not in signal_df.columns:
        signal_df = signal_df.rename(columns={"date": "timestamp"})
    
    price_df = price_df.copy().reset_index(drop=True)
    
    # Ensure both DataFrames are sorted by timestamp
    merged = pd.merge_asof(
        signal_df.sort_values("timestamp"),
        price_df.sort_values("timestamp"),
        on="timestamp",
        direction="backward"
    )
    
    return merged

if __name__ == "__main__":
    # Example usage:
    from datetime import datetime, timedelta
    import numpy as np

    # Create dummy price data
    dates = pd.date_range(start="2022-01-01", periods=100, freq='D')
    np.random.seed(42)
    prices = np.cumsum(np.random.randn(100)) + 100
    price_data = pd.DataFrame({
        'timestamp': dates,
        'high': prices + np.random.rand(100),
        'low': prices - np.random.rand(100),
        'close': prices
    })
    
    # Add technical indicators to price data
    price_with_features = add_ta_features(price_data)
    print("Price data with TA features:")
    print(price_with_features.head())
    
    # Create dummy signals data
    signals = pd.DataFrame({
        'date': [dates[10], dates[30], dates[50], dates[70]],
        'signal': ['buy', 'sell', 'buy', 'sell']
    })
    
    # Merge signals with price features
    merged_df = merge_signals(price_with_features, signals)
    print("\nMerged signals with features:")
    print(merged_df.head())

#!/usr/bin/env python3
"""
feature_engineering.py

Provides functions for:
1. Adding technical indicators (TA) to price data (RSI, Momentum, ATR, Bollinger, MACD, etc.).
2. Optionally building a synergy score from multiple signals or columns.
3. Merging external signal DataFrame(s) with the augmented price data.

Requires pandas_ta library for technical indicators, 
plus any synergy logic you decide to incorporate.
"""

import pandas as pd
import numpy as np
import pandas_ta as ta


def add_ta_features(df: pd.DataFrame,
                    add_macd: bool = True,
                    add_stoch: bool = True,
                    synergy_columns: list = None) -> pd.DataFrame:
    """
    Adds various technical indicators to a price DataFrame. 
    By default, it includes:
      - RSI (14)
      - Momentum (10)
      - ATR (14)
      - Bollinger Bands (20)
      - Keltner Channel (20)
      - MACD (12,26,9) if add_macd=True
      - Stochastics (14,3) if add_stoch=True

    Also, if synergy_columns is provided, we can build a "synergy_score"
    as the sum or average of those columns, or whichever logic you desire.

    Expects df to have at least columns: 'high','low','close'.
    If synergy_columns are specified, those must exist in df.

    Returns a new DataFrame with extra columns:
      'rsi', 'mom', 'atr', 'bb_upper','bb_middle','bb_lower',
      'keltner', 'macd', 'macd_signal','macd_hist', 'stoch_k','stoch_d',
      'price_above_bbands','price_below_bbands', 'synergy_score'(optional).
    """
    df = df.copy()

    # Basic TAs
    df["rsi"] = ta.rsi(df["close"], length=14)
    df["mom"] = ta.mom(df["close"], length=10)
    df["atr"] = ta.atr(df["high"], df["low"], df["close"], length=14)

    # Bollinger (20,2.0)
    bbands = ta.bbands(df["close"], length=20)
    df["bb_upper"] = bbands["BBU_20_2.0"]
    df["bb_middle"] = bbands["BBM_20_2.0"]
    df["bb_lower"] = bbands["BBL_20_2.0"]

    # Keltner
    kc = ta.kc(df["high"], df["low"], df["close"], length=20)
    # depending on your pandas_ta version, columns might differ
    # We'll assume the lower band is 'KCLe_20_2.0'
    df["keltner"] = kc["KCLe_20_2.0"]

    # Price vs Bollinger
    df["price_above_bbands"] = (df["close"] > df["bb_upper"]).astype(int)
    df["price_below_bbands"] = (df["close"] < df["bb_lower"]).astype(int)

    # Optional MACD
    if add_macd:
        macd_df = ta.macd(df["close"], fast=12, slow=26, signal=9)
        # macd_df has columns e.g. MACD_12_26_9, MACDs_12_26_9, MACDh_12_26_9
        df["macd"] = macd_df[macd_df.columns[0]]
        df["macd_signal"] = macd_df[macd_df.columns[1]]
        df["macd_hist"] = macd_df[macd_df.columns[2]]

    # Optional Stochastics
    if add_stoch:
        stoch_df = ta.stoch(df["high"], df["low"], df["close"], k=14, d=3)
        # stoch_df might have STOCHk_14_3_3, STOCHd_14_3_3
        stoch_cols = list(stoch_df.columns)
        df["stoch_k"] = stoch_df[stoch_cols[0]]
        df["stoch_d"] = stoch_df[stoch_cols[1]]

    # synergy aggregator - if user wants
    if synergy_columns is not None and len(synergy_columns) > 0:
        # Example: synergy_score = average of synergy_columns
        # or sum, or more advanced logic
        df["synergy_score"] = df[synergy_columns].mean(axis=1)
        # Alternatively, df["synergy_score"] = df[synergy_columns].sum(axis=1)

    return df


def merge_signals(price_df: pd.DataFrame,
                  signal_df: pd.DataFrame,
                  on_col: str = "timestamp",
                  how: str = "asof",
                  direction: str = "backward") -> pd.DataFrame:
    """
    Merge external signal DataFrame(s) with the price_df that already has
    TA features. Typically we do an "asof merge" so each signal row is matched 
    to the nearest previous price row.

    :param price_df: DataFrame with columns including the 'on_col' (usually 'timestamp') 
                     plus TA features
    :param signal_df: DataFrame with the same time col (on_col) or different name (we can rename).
                      May contain synergy/pivot flags or external signals.
    :param on_col: The column name to merge on (often 'timestamp' or 'datetime')
    :param how: 'asof' or 'merge' or 'left' or 'right', etc. If we want the 
                "most recent" approach, use asof with direction=backward/forward
    :param direction: for asof: 'backward','forward','nearest'
    :return: DataFrame with merged results
    """
    df_price = price_df.copy()
    df_signals = signal_df.copy()

    # ensure sorted
    df_price = df_price.sort_values(on_col).reset_index(drop=True)
    df_signals = df_signals.sort_values(on_col).reset_index(drop=True)

    if how == "asof":
        merged = pd.merge_asof(
            df_signals, df_price,
            on=on_col,
            direction=direction
        )
    else:
        # fallback standard merge
        merged = pd.merge(df_signals, df_price, on=on_col, how=how)

    return merged


def build_synergy_from_signals(signal_df: pd.DataFrame,
                               synergy_mapping: dict = None,
                               synergy_colname: str = "synergy_score") -> pd.DataFrame:
    """
    Given a DataFrame of signals, compute a synergy score per row 
    based on synergy_mapping. This is an optional tool for synergy generation.

    synergy_mapping could look like:
      {
        "demark_signal": 1.0,
        "pivot_signal": 1.5,
        "fundamental_buy": 2.0
      }
    Then synergy_score = sum of the columns * their weights if that column is 1 (or > 0).

    :param signal_df: DataFrame with columns for each discrete signal
    :param synergy_mapping: dict of {col_name -> weight}
    :param synergy_colname: str name for synergy score output
    :return: DataFrame with synergy_colname added
    """
    df = signal_df.copy()
    if synergy_mapping is None:
        synergy_mapping = {}

    synergy_scores = np.zeros(len(df))
    for col, weight in synergy_mapping.items():
        if col in df.columns:
            synergy_scores += df[col].astype(float) * weight

    df[synergy_colname] = synergy_scores
    return df


if __name__ == "__main__":
    # Example usage:
    from datetime import datetime, timedelta
    import numpy as np

    np.random.seed(42)

    # Create dummy price data
    dates = pd.date_range(start="2023-01-01", periods=50, freq='D')
    close_prices = 100 + np.cumsum(np.random.randn(50))
    df_price = pd.DataFrame({
        'timestamp': dates,
        'high': close_prices + 1.0,
        'low': close_prices - 1.0,
        'close': close_prices
    })

    # 1) Add TA features
    # let's do synergy_columns if we had e.g. 'volume' or 'another_signal' in df
    df_with_ta = add_ta_features(df_price,
                                add_macd=True,
                                add_stoch=True,
                                synergy_columns=None)  # none for now
    print("Added TA features:\n", df_with_ta.head())

    # 2) Suppose we have an external signal DataFrame
    signals = pd.DataFrame({
        'timestamp': dates[::5],  # every 5th day
        'demark_signal': np.random.randint(0,2, size=len(dates[::5])),
        'pivot_signal': np.random.randint(0,2, size=len(dates[::5]))
    })

    # create synergy if we want
    synergy_map = {
        "demark_signal": 1.0,
        "pivot_signal": 1.5
    }
    signals_synergy = build_synergy_from_signals(signals, synergy_map, synergy_colname="synergy_score")
    print("\nSignals with synergy:\n", signals_synergy.head())

    # 3) Merge signals with the TA-enhanced price data
    merged = merge_signals(df_with_ta, signals_synergy, on_col="timestamp", how="asof", direction="backward")
    print("\nMerged Data:\n", merged.head())

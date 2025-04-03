#!/usr/bin/env python3
"""
label_generation.py

Provides functions for generating and filtering labels (binary or multi-class) 
from future price movements. Allows flexible thresholds and label styles:
  1) Binary labeling
  2) Ternary (multi-class) labeling
  3) Optional continuous 'future_return' for regression tasks

Example usage:
  df_labeled = generate_labels(
      df=price_data,
      future_window=10,
      style='binary',
      upper_threshold=0.03,
      lower_threshold=-0.02
  )
  df_valid = filter_valid_labels(df_labeled)
"""

import pandas as pd
import numpy as np


def generate_labels(
    df: pd.DataFrame,
    future_window: int = 10,
    style: str = "binary",
    upper_threshold: float = 0.03,
    lower_threshold: float = -0.02,
    add_regression_label: bool = True
) -> pd.DataFrame:
    """
    Generate labels based on future returns.

    Steps:
      - We'll compute 'future_return' = (close.shift(-future_window) / close) - 1.0
      - Depending on 'style':
         * 'binary': label=1 if future_return >= upper_threshold, else 0 if future_return < upper_threshold 
                     (or if you want to incorporate lower_threshold, see below).
         * 'ternary': 
              label=2 if future_return >= upper_threshold
              label=1 if lower_threshold <= future_return < upper_threshold
              label=0 if future_return < lower_threshold

      - Optionally add 'future_return' as a column for potential regression tasks.

    :param df: DataFrame that has at least 'close' column
    :param future_window: how many bars to look ahead
    :param style: "binary" or "ternary" or "custom"
    :param upper_threshold: if future_return >= upper_threshold => bullish label
    :param lower_threshold: if future_return <= lower_threshold => bearish or 0 label
    :param add_regression_label: if True, keep 'future_return' for regression tasks
    :return: a copy of DataFrame with 'future_return' and 'label' columns
    """
    df = df.copy()
    if 'close' not in df.columns:
        raise ValueError("DataFrame must have a 'close' column to compute future_return.")

    # 1) compute future return
    df["future_return"] = df["close"].shift(-future_window) / df["close"] - 1.0

    # 2) define 'label' based on style
    if style not in ["binary", "ternary", "custom"]:
        raise ValueError("Unsupported style. Use 'binary', 'ternary', or 'custom'")

    df["label"] = np.nan  # start with NaN

    if style == "binary":
        # We'll do a simple approach:
        # label=1 if future_return >= upper_threshold, else 0
        # or you could incorporate a negative threshold => label=0 if future_return < 0 or < lower_threshold
        df.loc[df["future_return"] >= upper_threshold, "label"] = 1
        df.loc[df["future_return"] < upper_threshold, "label"] = 0

    elif style == "ternary":
        #  2 if future_return >= upper_threshold
        #  1 if lower_threshold <= future_return < upper_threshold
        #  0 if future_return < lower_threshold
        df.loc[df["future_return"] >= upper_threshold, "label"] = 2
        df.loc[(df["future_return"] < upper_threshold) &
               (df["future_return"] >= lower_threshold), "label"] = 1
        df.loc[df["future_return"] < lower_threshold, "label"] = 0

    else:
        # 'custom' => you can define your own labeling logic here or a callback
        # We'll just replicate the old logic:
        # label=1 if > upper_threshold, else 0 if < lower_threshold
        # if future_return in between, we do 0 or 1?
        # Let's replicate the old approach:
        df.loc[df["future_return"] > upper_threshold, "label"] = 1
        df.loc[df["future_return"] < lower_threshold, "label"] = 0
        # if user wants a do-nothing in the middle, it remains NaN

    # If add_regression_label is False, you might remove the 'future_return' column after labeling
    if not add_regression_label:
        df.drop(columns=["future_return"], inplace=True)

    return df


def filter_valid_labels(df: pd.DataFrame,
                        label_col: str = "label",
                        dropna_target: bool = True,
                        remove_leaks: bool = True,
                        future_window: int = 10) -> pd.DataFrame:
    """
    Remove rows with NaN labels or invalid future_return data to ensure only valid labeled data remains.

    Options:
      - dropna_target: if True, remove rows where 'label' is NaN
      - remove_leaks: if True, also remove the last `future_window` rows that cannot have valid future_return
        (since shift(-future_window) for them is NaN)
    :param df: DataFrame that includes a 'label' or label_col column.
    :param label_col: name of the label column
    :param dropna_target: bool, remove rows with label_col = NaN
    :param remove_leaks: bool, remove last future_window rows
    :param future_window: int, the window used for labeling
    :return: filtered DataFrame
    """
    df = df.copy()

    if dropna_target:
        df = df.dropna(subset=[label_col])

    if remove_leaks and future_window > 0:
        # If the user used shift(-future_window), 
        # the last future_window rows will have no valid future_return
        df = df.iloc[:-future_window] if len(df) > future_window else df.iloc[:0]

    return df


if __name__ == "__main__":
    from datetime import datetime
    import numpy as np

    # Demo with dummy data
    dates = pd.date_range(start="2022-01-01", periods=30, freq='D')
    np.random.seed(42)
    close_prices = 100 + np.cumsum(np.random.randn(30))
    df_data = pd.DataFrame({
        'datetime': dates,
        'close': close_prices
    })

    # Generate ternary labels with a 5-bar lookahead
    # upper_threshold=+3% => label=2
    # lower_threshold=-2% => label=0
    # else => label=1
    labeled = generate_labels(df_data,
                             future_window=5,
                             style='ternary',
                             upper_threshold=0.03,
                             lower_threshold=-0.02,
                             add_regression_label=True)
    print("Sample labeled data (ternary):\n", labeled.head(10))

    # Filter out invalid or last 5 rows
    filtered = filter_valid_labels(labeled, 
                                   label_col="label", 
                                   dropna_target=True,
                                   remove_leaks=True,
                                   future_window=5)
    print("\nFiltered data:\n", filtered.tail())

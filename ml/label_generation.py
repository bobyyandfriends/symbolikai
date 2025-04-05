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


def generate_labels(df: pd.DataFrame,
                    future_window: int = 5,
                    profit_threshold: float = 0.02,
                    loss_threshold: float = -0.01) -> pd.DataFrame:
    """
    Generates a binary classification label column based on future returns.

    Label = 1 if future return >= profit_threshold  
    Label = 0 if future return <= loss_threshold  
    Label = np.nan otherwise
    """
    df = df.copy()

    # Ensure we have sorted data
    df.sort_values("datetime", inplace=True)

    # Calculate future return
    df["future_price"] = df["close"].shift(-future_window)
    df["future_return"] = (df["future_price"] - df["close"]) / df["close"]

    # Assign label
    df["label"] = df["future_return"].apply(
        lambda r: 1 if r >= profit_threshold else (0 if r <= loss_threshold else None)
    )

    # Drop helper columns (optional)
    df.drop(columns=["future_price", "future_return"], inplace=True)

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

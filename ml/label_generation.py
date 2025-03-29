#!/usr/bin/env python3
import pandas as pd

def generate_labels(
    df: pd.DataFrame,
    future_window: int = 10,
    profit_threshold: float = 0.03,
    loss_threshold: float = -0.02,
) -> pd.DataFrame:
    """
    Generate binary labels based on future returns.

    Parameters:
      - df: DataFrame containing price data with a 'close' column.
      - future_window: Number of bars to look ahead.
      - profit_threshold: Threshold return above which label is 1.
      - loss_threshold: Threshold return below which label is set to 0.

    Returns:
      A copy of the DataFrame with added columns:
        'future_return' and 'label'
    """
    df = df.copy()
    # Calculate future return as a percentage change over the future_window
    df["future_return"] = df["close"].shift(-future_window) / df["close"] - 1.0

    # Default binary labels: 1 if future return exceeds profit threshold, else 0
    df["label"] = (df["future_return"] > profit_threshold).astype(int)

    # If the future return is less than the loss threshold, label it as 0
    if loss_threshold is not None:
        df.loc[df["future_return"] < loss_threshold, "label"] = 0

    return df

def filter_valid_labels(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows with NaN labels to ensure only valid labeled data remains.

    Parameters:
      - df: DataFrame that includes a 'label' column.

    Returns:
      DataFrame with rows missing 'label' removed.
    """
    df = df.copy()
    return df.dropna(subset=["label"])

if __name__ == "__main__":
    # Example usage:
    from datetime import datetime
    import numpy as np

    # Create dummy price data with a 'close' column
    dates = pd.date_range(start="2022-01-01", periods=50, freq='D')
    np.random.seed(42)
    prices = np.cumsum(np.random.randn(50)) + 100
    price_data = pd.DataFrame({
        'datetime': dates,
        'close': prices
    })

    # Generate labels with a 10-bar lookahead, 3% profit threshold, and -2% loss threshold
    labeled_data = generate_labels(price_data, future_window=10, profit_threshold=0.03, loss_threshold=-0.02)
    valid_data = filter_valid_labels(labeled_data)
    
    print("Labeled data sample:")
    print(valid_data.head())

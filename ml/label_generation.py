# ml/label_generation.py

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
    - future_window: number of bars to look ahead
    - profit_threshold: % return above which label is 1
    - loss_threshold: % return below which label is 0 (optional)

    Returns:
    - df with added 'label' column
    """
    df = df.copy()
    df["future_return"] = df["close"].shift(-future_window) / df["close"] - 1.0

    # Default binary labels
    df["label"] = (df["future_return"] > profit_threshold).astype(int)

    # Optional: remove or label high loss examples
    if loss_threshold is not None:
        df.loc[df["future_return"] < loss_threshold, "label"] = 0

    return df


def filter_valid_labels(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes rows with NaN labels or features after labeling.
    """
    df = df.copy()
    return df.dropna(subset=["label"])

# ml/feature_engineering.py

import pandas as pd
import pandas_ta as ta

def add_ta_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds TA indicators like RSI, Momentum, BBands, etc. to price data.
    """
    df = df.copy()

    df["rsi"] = ta.rsi(df["close"], length=14)
    df["mom"] = ta.mom(df["close"], length=10)
    df["atr"] = ta.atr(df["high"], df["low"], df["close"], length=14)
    df["bb_upper"], df["bb_middle"], df["bb_lower"] = ta.bbands(df["close"], length=20).values.T
    df["keltner"] = ta.kc(df["high"], df["low"], df["close"], length=20)["KCLe_20_2.0"]

    df["price_above_bbands"] = (df["close"] > df["bb_upper"]).astype(int)
    df["price_below_bbands"] = (df["close"] < df["bb_lower"]).astype(int)

    return df


def merge_signals(price_df: pd.DataFrame, signal_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merges signal timestamps with engineered features for model training.
    """
    signal_df = signal_df.copy()
    signal_df = signal_df.rename(columns={"date": "timestamp"})

    price_df = price_df.copy()
    price_df = price_df.reset_index()

    merged = pd.merge_asof(
        signal_df.sort_values("timestamp"),
        price_df.sort_values("timestamp"),
        on="timestamp",
        direction="backward"
    )

    return merged

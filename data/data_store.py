#!/usr/bin/env python3
import pandas as pd
import os


def save_df_csv(df: pd.DataFrame, path: str):
    """
    Save a DataFrame to a CSV file, overwriting any existing file.
    """
    df.to_csv(path, index=False)

def load_df_csv(path: str) -> pd.DataFrame:
    """
    Load a DataFrame from a CSV file, parsing 'datetime' as a date if present.
    By default parse_dates is True for all columns? We'll specifically parse 'datetime'.
    """
    # If 'datetime' might not exist, you can handle it. But let's assume it does.
    # We'll do something like:
    df = pd.read_csv(path)
    if 'datetime' in df.columns:
        df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
    return df

def save_df_pickle(df: pd.DataFrame, path: str):
    """
    Save a DataFrame to a pickle file for faster I/O.
    """
    df.to_pickle(path)

def load_df_pickle(path: str) -> pd.DataFrame:
    """
    Load a DataFrame from a pickle file.
    """
    return pd.read_pickle(path)

if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, 'example.csv')
    pickle_path = os.path.join(base_dir, 'example.pkl')

    # quick demonstration
    import numpy as np
    import datetime

    df_example = pd.DataFrame({
        'datetime': pd.date_range("2024-08-01 08:00:00", periods=5, freq='T'),
        'open': np.random.rand(5) + 223,
        'high': np.random.rand(5) + 224,
        'low': np.random.rand(5) + 222,
        'close': np.random.rand(5) + 223.5,
        'volume': np.random.randint(1000,2000,size=5)
    })

    save_df_csv(df_example, csv_path)
    print(f"[data_store] CSV saved to: {csv_path}")

    loaded_csv = load_df_csv(csv_path)
    print("[data_store] Loaded CSV sample:")
    print(loaded_csv.head())

    # test pickle
    save_df_pickle(df_example, pickle_path)
    loaded_pickle = load_df_pickle(pickle_path)
    print("[data_store] Loaded Pickle sample:")
    print(loaded_pickle.head())

import os
import pandas as pd
from typing import Union, IO

# def load_signals_from_file(path: str) -> pd.DataFrame:
#     """
#     Load raw signals from CSV or Excel.
#     """
#     ext = os.path.splitext(path)[1].lower()
#     if ext == '.csv':
#         df = pd.read_csv(path)
#     elif ext in ('.xls', '.xlsx'):
#         df = pd.read_excel(path)
#     else:
#         raise ValueError(f"[signal_loader] Unsupported file extension: {ext}")
#     return df
def load_signals_from_file(source: Union[str, IO]) -> pd.DataFrame:
    """
    Load signals from a file path or a file-like object (e.g. StringIO).
    Supports .csv and .json formats.
    """
    if isinstance(source, str):  # It's a path
        ext = os.path.splitext(source)[1].lower()
        if ext == ".csv":
            df = pd.read_csv(source)
        elif ext == ".json":
            df = pd.read_json(source)
        else:
            raise ValueError(f"Unsupported file extension: {ext}")
    else:  # Assume it's a file-like object (e.g., StringIO)
        df = pd.read_csv(source)  # You could enhance to detect .json if needed

    # Normalize column names if needed
    if "timestamp" in df.columns and "datetime" not in df.columns:
        df.rename(columns={"timestamp": "datetime"}, inplace=True)


def normalize_signals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert col names to lowercase, rename date->datetime, parse datetime, 
    standardize symbol and signal columns.
    """
    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]
    if 'date' in df.columns and 'datetime' not in df.columns:
        df.rename(columns={'date':'datetime'}, inplace=True)
    if 'datetime' in df.columns:
        df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
    else:
        raise KeyError("[signal_loader] Missing 'datetime' or 'date' in signals")

    if 'symbol' in df.columns:
        df['symbol'] = df['symbol'].astype(str).str.upper()
    else:
        raise KeyError("[signal_loader] Missing 'symbol' column in signals")

    if 'signal' in df.columns:
        df['signal'] = df['signal'].astype(str).str.lower()

    return df

def deduplicate_signals(existing_df: pd.DataFrame, new_df: pd.DataFrame) -> pd.DataFrame:
    """
    Combine existing + new, removing duplicates by symbol,signal,datetime
    """
    combined = pd.concat([existing_df, new_df], ignore_index=True)
    combined.drop_duplicates(subset=['symbol','signal','datetime'], inplace=True)
    combined.reset_index(drop=True, inplace=True)
    return combined

def save_master_signals(df: pd.DataFrame, path: str):
    """
    Save a final signals CSV.
    """
    df.to_csv(path, index=False)

if __name__ == "__main__":
    # Example usage
    pass

import pandas as pd

def normalize_signals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize signal formatting:
    - Rename columns
    - Format datetime
    - Clean text
    """
    df = df.copy()

    # Rename columns to standard format if needed
    rename_map = {
        "Date": "datetime",
        "Signal1": "signal_group",
        "Signal2": "signal_type",
        "Symbol": "symbol",
        "Exchange": "exchange",
        "Timeframe": "timeframe"
    }
    df.rename(columns=rename_map, inplace=True)

    # Parse datetime with flexibility
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
    df = df.dropna(subset=["datetime"])

    # Strip strings & uppercase symbols
    df["symbol"] = df["symbol"].str.upper().str.strip()
    df["signal_type"] = df["signal_type"].str.strip()
    df["signal_group"] = df["signal_group"].str.strip()
    df["exchange"] = df["exchange"].str.strip()
    df["timeframe"] = df["timeframe"].str.lower().str.strip()

    # Sort and reset
    df = df.sort_values(["symbol", "datetime"]).reset_index(drop=True)
    return df


def deduplicate_signals(existing_df: pd.DataFrame, new_df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes duplicates based on: symbol, datetime, signal_type, and timeframe.
    """
    combined = pd.concat([existing_df, new_df], ignore_index=True)

    deduped = combined.drop_duplicates(
        subset=["symbol", "datetime", "signal_type", "timeframe"]
    ).sort_values(["symbol", "datetime"])

    return deduped.reset_index(drop=True)


def save_master_signals(df: pd.DataFrame, path: str):
    """
    Save the combined master signal file to disk.
    """
    save_df_csv(df, path)

def load_master_signals(path: str) -> pd.DataFrame:
    """
    Load existing saved signals, if file exists.
    """
    if os.path.exists(path):
        return load_df_csv(path)
    else:
        return pd.DataFrame(columns=["symbol", "signal_group", "signal_type", "exchange", "timeframe", "datetime"])

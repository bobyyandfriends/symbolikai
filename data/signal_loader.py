import os
import pandas as pd

def load_signals_from_file(path: str) -> pd.DataFrame:
    """
    Load raw signals from an Excel or CSV file.
    The function detects the file extension and uses the appropriate pandas function.
    """
    ext = os.path.splitext(path)[1].lower()
    if ext == '.csv':
        df = pd.read_csv(path)
    elif ext in ['.xls', '.xlsx']:
        df = pd.read_excel(path)
    else:
        raise ValueError(f"Unsupported file extension for signals data: {ext}")
    return df

def normalize_signals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize the signals DataFrame:
    • Converts column names to lowercase and trims whitespace.
    • Renames common columns (e.g., 'date' to 'timestamp').
    • Parses timestamps to datetime objects.
    • Standardizes the symbol (upper-case) and signal (lower-case) columns.
    """
    df = df.copy()
    df.columns = [col.strip().lower() for col in df.columns]

    # Rename 'date' to 'timestamp' if needed
    if 'date' in df.columns and 'timestamp' not in df.columns:
        df.rename(columns={'date': 'timestamp'}, inplace=True)

    # Parse timestamp column
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    else:
        raise KeyError("The signals data must have a 'timestamp' or 'date' column.")

    # Standardize symbol column
    if 'symbol' in df.columns:
        df['symbol'] = df['symbol'].astype(str).str.strip().str.upper()
    else:
        raise KeyError("The signals data must have a 'symbol' column.")

    # Standardize signal column
    if 'signal' in df.columns:
        df['signal'] = df['signal'].astype(str).str.strip().str.lower()

    return df

def deduplicate_signals(existing_df: pd.DataFrame, new_df: pd.DataFrame) -> pd.DataFrame:
    """
    Combine the existing and new signal data while removing duplicates.
    Duplicates are defined based on 'symbol', 'signal', and 'timestamp'.
    """
    combined = pd.concat([existing_df, new_df], ignore_index=True)
    deduped = combined.drop_duplicates(subset=['symbol', 'signal', 'timestamp'])
    deduped.reset_index(drop=True, inplace=True)
    return deduped

def save_master_signals(df: pd.DataFrame, path: str):
    """
    Save the master signals DataFrame to a CSV file.
    """
    df.to_csv(path, index=False)

if __name__ == "__main__":
    # Example usage
    base_dir = os.path.dirname(__file__)
    new_signals_path = os.path.join(base_dir, "new_signals.csv")
    master_signals_path = os.path.join(base_dir, "master_signals.csv")

    try:
        new_df = load_signals_from_file(new_signals_path)
        new_df = normalize_signals(new_df)
        print("New signals loaded and normalized:")
        print(new_df.head())
    except Exception as e:
        print(f"Error loading new signals: {e}")
        new_df = pd.DataFrame()

    # Load existing master signals if available
    if os.path.exists(master_signals_path):
        master_df = pd.read_csv(master_signals_path, parse_dates=['timestamp'])
        master_df = normalize_signals(master_df)
    else:
        master_df = pd.DataFrame(columns=new_df.columns)

    # Deduplicate and combine
    combined_df = deduplicate_signals(master_df, new_df)
    print("Combined master signals (deduplicated):")
    print(combined_df.head())

    # Save the updated master signals
    save_master_signals(combined_df, master_signals_path)
    print(f"Master signals saved to: {master_signals_path}")

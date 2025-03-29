#!/usr/bin/env python3
import pandas as pd
import os

def save_df_csv(df: pd.DataFrame, path: str):
    """
    Save a DataFrame to a CSV file.
    This will overwrite any existing file at the given path.
    """
    df.to_csv(path, index=False)

def load_df_csv(path: str) -> pd.DataFrame:
    """
    Load a DataFrame from a CSV file.
    Assumes the CSV contains headers and parses date columns.
    """
    return pd.read_csv(path, parse_dates=True)

def save_df_pickle(df: pd.DataFrame, path: str):
    """
    Save a DataFrame to a pickle file.
    Pickle files allow for faster load times compared to CSV.
    """
    df.to_pickle(path)

def load_df_pickle(path: str) -> pd.DataFrame:
    """
    Load a DataFrame from a pickle file.
    """
    return pd.read_pickle(path)

if __name__ == "__main__":
    # Example usage:
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, 'example.csv')
    pickle_path = os.path.join(base_dir, 'example.pkl')
    
    df_example = pd.DataFrame({
        'A': [1, 2, 3],
        'B': ['x', 'y', 'z']
    })
    
    save_df_csv(df_example, csv_path)
    print("CSV saved to:", csv_path)
    loaded_csv = load_df_csv(csv_path)
    print("Loaded CSV:")
    print(loaded_csv.head())
    
    save_df_pickle(df_example, pickle_path)
    print("Pickle saved to:", pickle_path)
    loaded_pickle = load_df_pickle(pickle_path)
    print("Loaded Pickle:")
    print(loaded_pickle.head())

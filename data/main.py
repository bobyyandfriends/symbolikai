#!/usr/bin/env python3
import os
import pandas as pd
from data.collect_minute_data import update_symbol_data
from data.data_store import load_df_csv, save_df_csv

def update_all_symbols(universe_file: str, data_dir: str):
    """
    Read the tradeable universe file for symbols, update minute data for each symbol,
    and combine all symbol CSV files into one master CSV file.
    
    Parameters:
      universe_file: Path to a text file with one symbol per line.
      data_dir: Directory where minute data CSVs are stored.
    """
    if not os.path.exists(universe_file):
        print(f"Universe file not found: {universe_file}")
        return
    
    with open(universe_file, "r") as f:
        symbols = [line.strip() for line in f if line.strip()]
    
    # Ensure the data directory exists
    os.makedirs(data_dir, exist_ok=True)
    
    # Update data for each symbol
    for symbol in symbols:
        try:
            update_symbol_data(symbol)
        except Exception as e:
            print(f"Error updating data for {symbol}: {e}")
    
    # Combine all symbol CSV files into a master CSV
    master_data = []
    for symbol in symbols:
        symbol_csv = os.path.join(data_dir, f"{symbol.upper()}.csv")
        if os.path.exists(symbol_csv):
            try:
                df = load_df_csv(symbol_csv)
                df["symbol"] = symbol.upper()
                master_data.append(df)
            except Exception as e:
                print(f"Error loading data for {symbol} from {symbol_csv}: {e}")
    
    if master_data:
        combined_df = pd.concat(master_data, ignore_index=True)
        combined_df.sort_values("datetime", inplace=True)
        master_csv_path = os.path.join(data_dir, "master_minute_data.csv")
        save_df_csv(combined_df, master_csv_path)
        print(f"Master minute data saved to: {master_csv_path}")
    else:
        print("No data available to combine.")

def main():
    # Path to tradeable universe file (assumed to be in the project root)
    universe_file = os.path.join("..", "tradeable_universe.txt")
    # Directory where minute data CSVs are stored (inside the data folder)
    data_dir = os.path.join("data", "minute")
    update_all_symbols(universe_file, data_dir)

if __name__ == "__main__":
    main()

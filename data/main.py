#!/usr/bin/env python3
import os
import pandas as pd
import sys

# Dynamically add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_store import load_df_csv, save_df_csv

"""
This main.py can do:
  1) merges all minute CSV files from data/minute/ into one big CSV
  2) optionally read tradeable_universe.txt, call fetches (if you want),
     or you can rely on the separate script in collect_minute_data.py
"""

def update_all_symbols(universe_file: str, data_dir: str):
    """
    (Optional) For each symbol in universe_file, do the fetch routine 
    (like collect_minute_data.py does). We'll skip it if we rely on separate script.
    Then combine all data. This is an example approach:
    """

    # Example: we skip re-fetch because the 'collect_minute_data.py' is the main fetch script.
    # We'll just combine them:

    with open(universe_file, "r") as f:
        symbols = [line.strip() for line in f if line.strip()]

    master_data = []
    for sym in symbols:
        fpath = os.path.join(data_dir, f"{sym.upper()}_6mo_minute.csv")
        if os.path.exists(fpath):
            df = load_df_csv(fpath)
            if df.empty:
                continue
            # If you want the symbol column in master CSV, do:
            df["symbol"] = sym.upper()
            master_data.append(df)
        else:
            print(f"[main] No CSV found for {sym} at {fpath}")

    if master_data:
        combined_df = pd.concat(master_data, ignore_index=True)
        combined_df.sort_values("datetime", inplace=True)
        out_file = os.path.join(data_dir, "master_minute_data.csv")
        save_df_csv(combined_df, out_file)
        print(f"[main] Master CSV saved => {out_file}")
    else:
        print("[main] No data to combine into master CSV.")

def main():
    # usage example
    universe_file = "tradeable_universe.txt"
    data_dir = os.path.join("data", "minute")
    if not os.path.exists(universe_file):
        print(f"[main] Universe file not found: {universe_file}")
        return

    # combine
    update_all_symbols(universe_file, data_dir)

if __name__ == "__main__":
    main()

import os
import pandas as pd
import sys

# Dynamically add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


"""
min_to_other.py
If you want to resample your minute data into different intervals (2min,5min,...),
this script finds CSVs in polygon_minute_data/ and outputs them to polygon_2min_data, etc.
We'll keep it as is, but ensure columns are [datetime,open,high,low,close,volume].
"""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FOLDER = os.path.join(BASE_DIR, "minute_data")  # instead of polygon_minute_data
OUTPUT_INTERVALS = {
    "2min": os.path.join(BASE_DIR, "2min_data"),
    "5min": os.path.join(BASE_DIR, "5min_data"),
    "10min": os.path.join(BASE_DIR, "10min_data"),
    "15min": os.path.join(BASE_DIR, "15min_data"),
    "30min": os.path.join(BASE_DIR, "30min_data"),
    "60min": os.path.join(BASE_DIR, "60min_data"),
    "90min": os.path.join(BASE_DIR, "90min_data"),
    "120min": os.path.join(BASE_DIR, "120min_data"),
    "180min": os.path.join(BASE_DIR, "180min_data"),
    "240min": os.path.join(BASE_DIR, "240min_data"),
    "D": os.path.join(BASE_DIR, "daily_data"),
    "W": os.path.join(BASE_DIR, "weekly_data"),
}


ohlc_dict = {
    'open': 'first',
    'high': 'max',
    'low': 'min',
    'close': 'last',
    'volume': 'sum'
}

for folder in OUTPUT_INTERVALS.values():
    os.makedirs(folder, exist_ok=True)

for filename in os.listdir(INPUT_FOLDER):
    if filename.endswith(".csv"):
        filepath = os.path.join(INPUT_FOLDER, filename)
        df = pd.read_csv(filepath)
        # parse date
        if 'datetime' in df.columns:
            df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
        else:
            print(f"[min_to_other] No 'datetime' column in {filename}, skipping.")
            continue

        df.set_index('datetime', inplace=True)

        for freq, out_folder in OUTPUT_INTERVALS.items():
            resampled = df.resample(freq).apply(ohlc_dict).dropna()
            resampled.reset_index(inplace=True)

            # Strip extension and infer symbol name from filename
            symbol = filename.split("_")[0]  # Gets 'AAPL' from 'AAPL_6mo_minute.csv'

            # Define new filename using symbol and timeframe
            new_filename = f"{symbol}_{freq}.csv"

            out_path = os.path.join(out_folder, new_filename)
            resampled.to_csv(out_path, index=False)

            print(f"[min_to_other] Saved {freq} data => {out_path}")

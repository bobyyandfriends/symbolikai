import os
import pandas as pd

# Automatically get the path of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FOLDER = os.path.join(BASE_DIR, "polygon_minute_data")
OUTPUT_INTERVALS = {
    "2min": os.path.join(BASE_DIR, "polygon_2min_data"),
    "5min": os.path.join(BASE_DIR, "polygon_5min_data"),
    "10min": os.path.join(BASE_DIR, "polygon_10min_data"),
    "15min": os.path.join(BASE_DIR, "polygon_15min_data"),
    "30min": os.path.join(BASE_DIR, "polygon_30min_data"),
    "60min": os.path.join(BASE_DIR, "polygon_60min_data"),
    "90min": os.path.join(BASE_DIR, "polygon_90min_data"),
    "120min": os.path.join(BASE_DIR, "polygon_120min_data"),
    "180min": os.path.join(BASE_DIR, "polygon_180min_data"),
    "240min": os.path.join(BASE_DIR, "polygon_240min_data"),
    "D": os.path.join(BASE_DIR, "polygon_daily_data"),
    "W": os.path.join(BASE_DIR, "polygon_weekly_data"),
}


# Resampling dictionary
ohlc_dict = {
    'open': 'first',
    'high': 'max',
    'low': 'min',
    'close': 'last',
    'volume': 'sum'
}

# Create output folders if they don’t exist
for folder in OUTPUT_INTERVALS.values():
    os.makedirs(folder, exist_ok=True)

# Process all CSV files in the input folder
for filename in os.listdir(INPUT_FOLDER):
    if filename.endswith(".csv"):
        filepath = os.path.join(INPUT_FOLDER, filename)
        df = pd.read_csv(filepath, parse_dates=['timestamp'])

        # Set timestamp as index
        df.set_index('timestamp', inplace=True)

        for freq, out_folder in OUTPUT_INTERVALS.items():
            resampled = df.resample(freq).apply(ohlc_dict).dropna()
            resampled.reset_index(inplace=True)

            out_path = os.path.join(out_folder, filename)
            resampled.to_csv(out_path, index=False)
            print(f"Saved {freq} data to {out_path}")

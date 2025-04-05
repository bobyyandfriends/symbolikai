import os
import pandas as pd

DATA_DIR = "data"  # relative path to your data folder

def rename_timestamp_column(file_path):
    try:
        df = pd.read_csv(file_path)
        if "timestamp" in df.columns:
            df.rename(columns={"timestamp": "datetime"}, inplace=True)
            df.to_csv(file_path, index=False)
            print(f"✅ Updated: {file_path}")
        else:
            print(f"❌ Skipped (no 'timestamp' column): {file_path}")
    except Exception as e:
        print(f"❗ Error with {file_path}: {e}")

def process_all_csv_files(data_dir):
    for root, _, files in os.walk(data_dir):
        for file in files:
            if file.endswith(".csv"):
                full_path = os.path.join(root, file)
                rename_timestamp_column(full_path)

if __name__ == "__main__":
    process_all_csv_files(DATA_DIR)

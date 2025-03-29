# data/collect_minute_data.py

import os
import pandas as pd
from datetime import datetime, timedelta
import requests  # you'll need this for real API calls
from data.data_store import save_df_csv, load_df_csv

# === CONFIGURATION ===
# Set your API key and endpoint (modify as needed for your provider)
API_KEY = "YOUR_API_KEY_HERE"
API_ENDPOINT = "https://api.example.com/minute_data"  # Replace with real endpoint

# Path to the tradeable universe list
SYMBOL_LIST_FILE = os.path.join("..", "tradeable_universe.txt")

# Directory to store minute data CSVs
DATA_DIR = os.path.join("data", "minute")

def fetch_minute_data(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetch 1-minute OHLCV data from the API for the given symbol and date range.
    Replace this stub with your provider-specific API call.
    """
    # Example parameters (customize as needed)
    params = {
        "symbol": symbol,
        "start": start_date,
        "end": end_date,
        "api_key": API_KEY,
    }
    
    # For now, we simulate a response
    # In practice, you'd do:
    # response = requests.get(API_ENDPOINT, params=params)
    # data = response.json()
    # Then convert data to a DataFrame.
    print(f"Fetching data for {symbol} from {start_date} to {end_date}...")
    
    # Simulated data for demonstration:
    dt_range = pd.date_range(start=start_date, end=end_date, freq="1min")
    data = {
        "datetime": dt_range,
        "symbol": symbol,
        "open": 100 + pd.np.random.rand(len(dt_range)),
        "high": 100 + pd.np.random.rand(len(dt_range)),
        "low": 100 + pd.np.random.rand(len(dt_range)),
        "close": 100 + pd.np.random.rand(len(dt_range)),
        "volume": pd.np.random.randint(100, 1000, size=len(dt_range))
    }
    df = pd.DataFrame(data)
    return df

def update_symbol_data(symbol: str):
    """
    For a given symbol, fetch new minute data from the latest timestamp
    in the existing CSV (if any) until today, and append to CSV.
    """
    csv_path = os.path.join(DATA_DIR, f"{symbol.upper()}.csv")
    
    # Determine the start date for fetching new data:
    if os.path.exists(csv_path):
        existing_df = load_df_csv(csv_path)
        last_date = existing_df["datetime"].max()
        # Start fetching from the next minute after the last recorded
        start_date = (pd.to_datetime(last_date) + timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M:%S")
    else:
        # If no data exists, define a default start date (e.g., one week ago)
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
        existing_df = pd.DataFrame()

    # Fetch data until now (end_date)
    end_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    new_data = fetch_minute_data(symbol, start_date, end_date)
    if not existing_df.empty:
        combined_df = pd.concat([existing_df, new_data], ignore_index=True)
    else:
        combined_df = new_data

    # Remove duplicates, sort by datetime
    combined_df = combined_df.drop_duplicates(subset=["datetime"]).sort_values("datetime")
    save_df_csv(combined_df, csv_path)
    print(f"Data updated for {symbol}.")

def main():
    # Read symbols from the tradeable universe file
    with open(SYMBOL_LIST_FILE, "r") as f:
        symbols = [line.strip() for line in f if line.strip()]
    
    # Ensure the DATA_DIR exists
    os.makedirs(DATA_DIR, exist_ok=True)
    
    for symbol in symbols:
        try:
            update_symbol_data(symbol)
        except Exception as e:
            print(f"Error updating {symbol}: {e}")

if __name__ == "__main__":
    main()

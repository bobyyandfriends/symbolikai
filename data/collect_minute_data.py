#!/usr/bin/env python3
"""
collect_minute_data.py

Pull minute-level OHLCV data from Polygon.io for each symbol listed in a text file
(called "tradeable_universe.txt"). Data is fetched in chunks to avoid large calls, 
and each final CSV is stored in data/minute/<SYMBOL>.csv with columns:
  timestamp,open,high,low,close,volume
No 'symbol' column is stored in each CSV.

Key variables:
  START_DAYS_AGO: e.g. 240 (8 months)
  CHUNK_DAYS: how many days per chunk
  SLEEP_BETWEEN_CALLS: seconds to sleep to respect rate limit
"""

import requests
import pandas as pd
import time
import os
from datetime import datetime, timedelta
from data.data_store import save_df_csv, load_df_csv

# === CONFIG ===
API_KEY = "axGISBpI_t8pxtKOTRB6mdmcovNLpZjx"  # Replace with your actual Polygon.io key
SAVE_DIR = "minute_data"
START_DAYS_AGO = 240        # e.g. ~8 months of data
CHUNK_DAYS = 120            # 2 chunks of 120 days each
SLEEP_BETWEEN_CALLS = 12    # seconds to respect 5 calls/min limit

def fetch_minute_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetch 1-minute OHLCV data from Polygon's Aggregates API.
    Endpoint: https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/minute/{start}/{end}

    Returns a DataFrame with columns:
      timestamp, open, high, low, close, volume
    """
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/minute/{start_date}/{end_date}"
    params = {
        "adjusted": "true",
        "sort": "asc",
        "limit": 50000,
        "apiKey": API_KEY
    }
    print(f"[→] Fetching {ticker} from {start_date} to {end_date}")
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"[!] Error for {ticker}: {response.status_code} {response.text}")
        return pd.DataFrame()

    data = response.json()
    if 'results' not in data:
        print(f"[!] No results for {ticker}")
        return pd.DataFrame()

    df = pd.DataFrame(data['results'])
    # convert 't' to datetime
    df['timestamp'] = pd.to_datetime(df['t'], unit='ms')
    # rename columns
    df = df.rename(columns={
        'o': 'open', 'h': 'high', 'l': 'low', 'c': 'close', 'v': 'volume'
    })
    # keep only final columns
    df = df[['timestamp','open','high','low','close','volume']]
    return df

def fetch_and_save_symbol(ticker: str):
    """
    For a single symbol, chunk the date range, fetch data, 
    combine, deduplicate, and store in CSV:
      data/minute/<TICKER>_6mo_minute.csv
    """
    os.makedirs(SAVE_DIR, exist_ok=True)

    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=START_DAYS_AGO)

    symbol_df = pd.DataFrame()
    # chunk-based approach
    for i in range(0, START_DAYS_AGO, CHUNK_DAYS):
        chunk_start = start_date + timedelta(days=i)
        chunk_end = min(chunk_start + timedelta(days=CHUNK_DAYS), end_date)

        df = fetch_minute_data(
            ticker,
            chunk_start.strftime('%Y-%m-%d'),
            chunk_end.strftime('%Y-%m-%d')
        )
        if not df.empty:
            symbol_df = pd.concat([symbol_df, df], ignore_index=True)

        time.sleep(SLEEP_BETWEEN_CALLS)

    if not symbol_df.empty:
        # sort & deduplicate
        symbol_df.drop_duplicates(subset=["timestamp"], inplace=True)
        symbol_df.sort_values("timestamp", inplace=True)

        file_path = os.path.join(SAVE_DIR, f"{ticker.upper()}_minute.csv")
        save_df_csv(symbol_df, file_path)
        print(f"[✓] Saved {ticker} data to {file_path}")
    else:
        print(f"[!] No data saved for {ticker}")

def main():
    """
    1) read the text file for tickers
    2) fetch & save each symbol's minute data
    """
    TICKER_LIST_FILE = "tradeable_universe.txt"  # or specify a path
    if not os.path.exists(TICKER_LIST_FILE):
        print(f"[!] Ticker list file not found: {TICKER_LIST_FILE}")
        return

    with open(TICKER_LIST_FILE, "r") as f:
        tickers = [line.strip() for line in f if line.strip()]

    for sym in tickers:
        fetch_and_save_symbol(sym)

if __name__ == "__main__":
    main()

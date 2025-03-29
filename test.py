

import requests
import pandas as pd
import time
import os
from datetime import datetime, timedelta

# === CONFIG ===
API_KEY = "axGISBpI_t8pxtKOTRB6mdmcovNLpZjx"  # 🔁 Replace with your actual Polygon.io API key
SAVE_DIR = "polygon_minute_data"
START_DAYS_AGO = 240           # Pull 6 months of data
CHUNK_DAYS = 120               # Two 120-day chunks
SLEEP_BETWEEN_CALLS = 12       # Respect 5 calls/minute limit

# === YOUR SYMBOL LIST ===
SYMBOLS = [
    "ORCL", "PKX", "SYNA", "TDC",
    "TER", "VRT", "WDC", "AMAT", "AMKR", "AMZN", "ANET", "AVGO", "GOOG", "IBM", "INTC", "LRCX",
    "MSFT", "NOW", "NVDA", "PATH", "PDFS", "SKYT", "TSEM", "REE", "META", "PX", "AAPL", "DELL",
    "SMCI", "APH", "HPE", "KEYS", "PSTG", "CLS", "GLW", "JBL", "TSLA", "PLTR", "UBER", "CAMT",
    "CRWD", "FCX", "PWR", "ATRO", "FLEX", "VIAV", "NTNX", "COMP", "COMM", "AMD", "EXTR"
]

# === Fetch Minute Data from Polygon ===
def fetch_minute_data(ticker, start_date, end_date):
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
    df['timestamp'] = pd.to_datetime(df['t'], unit='ms')
    df = df.rename(columns={
        'o': 'open', 'h': 'high', 'l': 'low', 'c': 'close', 'v': 'volume'
    })[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
    return df

# === Main Logic ===
def main():
    os.makedirs(SAVE_DIR, exist_ok=True)

    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=START_DAYS_AGO)

    for symbol in SYMBOLS:
        symbol_df = pd.DataFrame()
        for i in range(0, START_DAYS_AGO, CHUNK_DAYS):
            chunk_start = start_date + timedelta(days=i)
            chunk_end = min(chunk_start + timedelta(days=CHUNK_DAYS), end_date)

            df = fetch_minute_data(
                symbol,
                chunk_start.strftime('%Y-%m-%d'),
                chunk_end.strftime('%Y-%m-%d')
            )
            if not df.empty:
                symbol_df = pd.concat([symbol_df, df], ignore_index=True)

            time.sleep(SLEEP_BETWEEN_CALLS)

        if not symbol_df.empty:
            file_path = os.path.join(SAVE_DIR, f"{symbol}_6mo_minute.csv")
            symbol_df.to_csv(file_path, index=False)
            print(f"[✓] Saved {symbol} data to {file_path}")
        else:
            print(f"[!] No data saved for {symbol}")

if __name__ == "__main__":
    main()

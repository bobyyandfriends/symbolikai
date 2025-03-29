# 📁 data/

This module handles all aspects of data ingestion, normalization, and storage for the SymbolikAI system. It includes utilities for loading and saving price data, processing DeMark signals, and managing symbol watchlists or filters.

---

## 🧱 Folder Structure

```
data/
├── __init__.py
├── pricing_loader.py
├── signal_loader.py
├── data_store.py
├── symbol_filter.py
├── collect_minute_data.py
└── minute/
    └── <symbol>.csv
```

---

## 📄 File Descriptions

### `__init__.py`
- Marks the folder as a Python package. No logic inside.

---

### `pricing_loader.py`
Handles loading and optionally resampling historical OHLCV price data from disk.

**Functions:**
- `load_price_data(symbol: str, timeframe: str) -> pd.DataFrame`: Loads OHLCV data from CSV for a given symbol/timeframe.
- `get_price_path(symbol: str, timeframe: str) -> str`: Constructs the local path to the symbol's data file.
- `resample_price_data(df: pd.DataFrame, timeframe: str) -> pd.DataFrame`: Converts 1-min data to higher granularity like 240-min or daily (optional).

---

### `signal_loader.py`
Loads and manages DeMark signal data files from CSV/Excel and merges them with the master list.

**Functions:**
- `load_signals_from_file(path: str)`: Load raw signal data.
- `normalize_signals(df: pd.DataFrame)`: Standardize column names, timestamps, signal types.
- `deduplicate_signals(existing_df, new_df)`: Removes duplicates based on symbol/signal/timestamp.
- `save_master_signals(df, path)`: Saves merged dataset.

---

### `data_store.py`
Generic helpers for saving/loading DataFrames in various formats.

**Functions:**
- `save_df_csv(df, path)`
- `load_df_csv(path)`
- `save_df_pickle(df, path)`
- `load_df_pickle(path)`

---

### `symbol_filter.py`
Filters the tradeable universe by activity or user-defined watchlists.

**Functions:**
- `get_watchlist(name: str) -> List[str]`: Load tickers from watchlist file.
- `filter_symbols_by_activity(date: str) -> List[str]`: Return tickers active on a certain date.

---

### `collect_minute_data.py`
Pulls 1-minute OHLCV data for all symbols in `tradeable_universe.txt`, appends missing rows, and stores them in the `/data/minute/` directory.

**Highlights:**
- Integrates with Polygon.io, Alpaca, or another data provider.
- Logs API errors.
- Avoids duplicate fetches.
- Supports compression and CLI options for future extensibility.

---

### `minute/` Folder
Stores 1-minute data for each symbol in individual CSV files with:
```
datetime, symbol, open, high, low, close, volume
```

---

## 🧠 Design Philosophy

- Prefer fast local access (CSV + optional Pickle).
- Build reusable loaders that support batch runs and interactive notebooks.
- Normalize all timestamps and signal types upfront.
- Prepare for eventual multi-source ingestion and cloud migration.

---

## 🔮 Future Ideas

- Add support for downloading daily data directly from APIs.
- Create a symbol metadata system for fundamentals, sectors, etc.
- Integrate data quality checks (e.g., gap detection).
- Extend resampling logic for 5-min, 30-min, and other granularities.
#!/usr/bin/env python3
import pytest
import pandas as pd
import io
from data.pricing_loader import load_price_data, get_price_path, resample_price_data
from data.signal_loader import load_signals_from_file, normalize_signals, deduplicate_signals
import os

@pytest.fixture
def dummy_price_csv(tmp_path):
    data = {
        "datetime": pd.date_range(start="2022-01-01", periods=10, freq="D"),
        "open": [100 + i for i in range(10)],
        "high": [101 + i for i in range(10)],
        "low": [99 + i for i in range(10)],
        "close": [100 + i for i in range(10)],
        "volume": [1000 + 10 * i for i in range(10)]
    }
    df = pd.DataFrame(data)
    file_path = tmp_path / "AAPL_daily.csv"
    df.to_csv(file_path, index=False)
    return file_path, df

def test_get_price_path(tmp_path):
    # Create a fake price_data directory inside tmp_path
    price_data_dir = tmp_path / "price_data"
    price_data_dir.mkdir()
    file_path = price_data_dir / "AAPL_daily.csv"
    pd.DataFrame({"dummy": [1]}).to_csv(file_path, index=False)
    # Monkey-patch get_price_path to use our temporary directory
    from data import pricing_loader
    original_get_price_path = pricing_loader.get_price_path
    pricing_loader.get_price_path = lambda symbol, timeframe: str(file_path)
    try:
        loaded_df = load_price_data("AAPL", "daily")
        assert "close" in loaded_df.columns
    finally:
        pricing_loader.get_price_path = original_get_price_path

def test_resample_price_data(dummy_price_csv):
    _, original_df = dummy_price_csv
    resampled_df = resample_price_data(original_df, "W")
    # Weekly resampling should yield fewer rows than daily data.
    assert len(resampled_df) < len(original_df)

def dummy_signal_csv():
    csv_content = """date,Symbol,Signal
2022-01-01,AAPL,buy
2022-01-02,AAPL,sell
2022-01-03,MSFT,buy
2022-01-04,MSFT,sell
"""
    return io.StringIO(csv_content)

def test_load_and_normalize_signals():
    f = dummy_signal_csv()
    df = load_signals_from_file(f)
    norm_df = normalize_signals(df)
    assert "datetime" in norm_df.columns
    # Symbol should be uppercase after normalization.
    assert norm_df["symbol"].iloc[0] == "AAPL"

def test_deduplicate_signals():
    data1 = {
        "datetime": pd.to_datetime(["2022-01-01", "2022-01-02"]),
        "symbol": ["AAPL", "AAPL"],
        "signal": ["buy", "sell"]
    }
    data2 = {
        "datetime": pd.to_datetime(["2022-01-02", "2022-01-03"]),
        "symbol": ["AAPL", "MSFT"],
        "signal": ["sell", "buy"]
    }
    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)
    combined = deduplicate_signals(df1, df2)
    # There should be three unique rows after deduplication.
    assert combined.shape[0] == 3

if __name__ == "__main__":
    pytest.main()

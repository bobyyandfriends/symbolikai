#!/usr/bin/env python3
import pandas as pd
import pytest
import os
import sys

# Dynamically add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.pricing_loader import load_price_data, get_price_path, resample_price_data

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
    price_dir = tmp_path / "price_data"
    price_dir.mkdir()
    file_path = price_dir / "AAPL_daily.csv"
    pd.DataFrame({"dummy": [1]}).to_csv(file_path, index=False)
    path = get_price_path("AAPL", "daily")
    assert path.endswith("AAPL_daily.csv")

def test_load_price_data(dummy_price_csv, monkeypatch):
    file_path, original_df = dummy_price_csv
    def fake_get_price_path(symbol, timeframe):
        return str(file_path)
    monkeypatch.setattr("data.pricing_loader.get_price_path", fake_get_price_path)
    loaded_df = load_price_data("AAPL", "daily")
    pd.testing.assert_series_equal(loaded_df["close"], original_df["close"])

def test_resample_price_data(dummy_price_csv):
    _, original_df = dummy_price_csv
    resampled_df = resample_price_data(original_df, "W")
    assert len(resampled_df) < len(original_df)

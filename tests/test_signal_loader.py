#!/usr/bin/env python3
import pandas as pd
import io
import pytest
from data.signal_loader import load_signals_from_file, normalize_signals, deduplicate_signals

def dummy_csv_data():
    csv_content = """Date,Symbol,Signal
2022-01-01,AAPL,buy
2022-01-02,AAPL,sell
2022-01-03,MSFT,buy
2022-01-04,MSFT,sell
"""
    return io.StringIO(csv_content)

def test_load_signals_from_csv():
    f = dummy_csv_data()
    df = load_signals_from_file(f)
    # Expect a column named "date" or "datetime" (which will be renamed later)
    assert any(col in df.columns for col in ["date", "datetime"])

def test_normalize_signals():
    f = dummy_csv_data()
    df = load_signals_from_file(f)
    norm_df = normalize_signals(df)
    # After normalization, there should be a "datetime" and "symbol" in uppercase.
    assert "datetime" in norm_df.columns
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
    # Expect three unique rows after deduplication.
    assert combined.shape[0] == 3

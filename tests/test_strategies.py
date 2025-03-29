#!/usr/bin/env python3
import pandas as pd
import numpy as np
import pytest
from datetime import datetime
from strategies.simple_strategy import SimpleStrategy
from strategies.demark_perfection_strategy import DemarkPerfectionStrategy
from strategies.combo_strategy_example import ComboStrategyExample

@pytest.fixture
def dummy_price_data():
    dates = pd.date_range(start="2022-01-01", periods=50, freq="D")
    np.random.seed(42)
    prices = np.cumsum(np.random.randn(50)) + 100
    data = pd.DataFrame({
        "datetime": dates,
        "open": prices + np.random.randn(50)*0.5,
        "high": prices + np.random.rand(50),
        "low": prices - np.random.rand(50),
        "close": prices,
        "volume": np.random.randint(100, 1000, size=50)
    })
    return data

@pytest.fixture
def simple_strategy():
    return SimpleStrategy()

@pytest.fixture
def perfection_strategy():
    return DemarkPerfectionStrategy()

@pytest.fixture
def combo_strategy():
    return ComboStrategyExample()

def test_simple_strategy_signals(simple_strategy, dummy_price_data):
    signals = simple_strategy.generate_signals(dummy_price_data)
    assert "datetime" in signals.columns and "signal" in signals.columns

def test_simple_strategy_trades(simple_strategy, dummy_price_data):
    signals = simple_strategy.generate_signals(dummy_price_data)
    trades = simple_strategy.generate_trades(dummy_price_data, signals)
    if not trades.empty:
        expected_cols = {"entry_time", "entry_price", "exit_time", "exit_price", "profit"}
        assert expected_cols.issubset(set(trades.columns))

def test_perfection_strategy(perfection_strategy, dummy_price_data):
    signals = perfection_strategy.generate_signals(dummy_price_data)
    assert "datetime" in signals.columns and "signal" in signals.columns

def test_combo_strategy(combo_strategy, dummy_price_data):
    signals = combo_strategy.generate_signals(dummy_price_data)
    assert "datetime" in signals.columns and "signal" in signals.columns

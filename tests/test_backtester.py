#!/usr/bin/env python3
import pytest
import pandas as pd
import numpy as np
from datetime import datetime
from backtest.backtester import run_backtest
from strategies.simple_strategy import SimpleStrategy

@pytest.fixture
def dummy_price_data():
    """
    Create dummy historical price data with necessary columns.
    """
    dates = pd.date_range(start="2022-01-01", periods=50, freq='D')
    np.random.seed(42)
    prices = np.cumsum(np.random.randn(50)) + 100
    data = pd.DataFrame({
        'datetime': dates,
        'open': prices + np.random.randn(50) * 0.5,
        'high': prices + np.random.rand(50),
        'low': prices - np.random.rand(50),
        'close': prices,
        'volume': np.random.randint(100, 1000, size=50)
    })
    return data

@pytest.fixture
def dummy_strategy():
    """
    Provide an instance of SimpleStrategy.
    """
    from strategies.simple_strategy import SimpleStrategy
    return SimpleStrategy()

@pytest.fixture
def dummy_signals(dummy_price_data, dummy_strategy):
    """
    Generate dummy signals using the dummy strategy.
    """
    return dummy_strategy.generate_signals(dummy_price_data)

def test_run_backtest(dummy_price_data, dummy_strategy, dummy_signals):
    """
    Test run_backtest returns a valid results dictionary.
    """
    config = {"initial_capital": 100000}
    results = run_backtest(dummy_strategy, dummy_price_data, dummy_signals, config)
    
    # Check that results is a dictionary with expected keys.
    expected_keys = {"trades", "metrics", "config", "strategy_name", "timestamp"}
    assert expected_keys.issubset(results.keys())
    
    # Check that trades is a DataFrame with expected columns, if not empty.
    trades = results["trades"]
    assert isinstance(trades, pd.DataFrame)
    if not trades.empty:
        expected_trade_columns = {"entry_time", "entry_price", "exit_time", "exit_price", "profit"}
        assert expected_trade_columns.issubset(set(trades.columns))
    
    # Check that metrics is a dictionary with key performance indicators.
    metrics = results["metrics"]
    expected_metric_keys = {"total_return", "win_rate", "avg_profit", "max_drawdown", "num_trades"}
    assert expected_metric_keys.issubset(set(metrics.keys()))
    
    # Verify strategy name matches the dummy strategy.
    assert results["strategy_name"] == dummy_strategy.name

if __name__ == "__main__":
    pytest.main()

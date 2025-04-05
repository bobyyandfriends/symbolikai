#!/usr/bin/env python3
import pytest
import pandas as pd
from datetime import datetime
import os
import sys

# Dynamically add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backtest.metrics import calculate_metrics

def dummy_trades():
    trades_data = [
        {
            'entry_time': datetime(2022, 1, 1),
            'entry_price': 100,
            'exit_time': datetime(2022, 1, 5),
            'exit_price': 105,
            'profit': 5
        },
        {
            'entry_time': datetime(2022, 1, 10),
            'entry_price': 106,
            'exit_time': datetime(2022, 1, 15),
            'exit_price': 104,
            'profit': -2
        },
        {
            'entry_time': datetime(2022, 1, 20),
            'entry_price': 103,
            'exit_time': datetime(2022, 1, 25),
            'exit_price': 108,
            'profit': 5
        }
    ]
    return pd.DataFrame(trades_data)

def test_calculate_metrics():
    trades = dummy_trades()
    initial_capital = 100000
    metrics = calculate_metrics(trades, initial_capital)
    
    expected_keys = {"total_return_percent", "win_rate_percent", "avg_profit", "max_drawdown_percent", "num_trades", "avg_holding_days"}
    assert expected_keys.issubset(set(metrics.keys()))
    
    total_profit = sum(trade["profit"] for trade in trades.to_dict("records"))
    expected_total_return = (total_profit / initial_capital) * 100
    assert metrics["total_return_percent"] == pytest.approx(expected_total_return)
    
    # With 2 winning trades out of 3, win rate ~66.67%
    assert metrics["win_rate_percent"] == pytest.approx((2/3)*100, rel=0.01)
    assert metrics["num_trades"] == 3

if __name__ == "__main__":
    pytest.main()

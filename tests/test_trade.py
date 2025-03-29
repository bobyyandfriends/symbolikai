#!/usr/bin/env python3
import pytest
import pandas as pd
from datetime import datetime, timedelta
from backtest.trade import Trade

def test_long_trade_pnl():
    entry_time = datetime(2022, 1, 1, 9, 30)
    exit_time = entry_time + timedelta(hours=6)
    entry_price = 100.0
    exit_price = 105.0
    trade = Trade(entry_time, entry_price, side="long", slippage_pct=0.0)
    trade.close_trade(exit_time, exit_price)
    # For a long trade, profit should equal exit - entry
    assert trade.pnl == pytest.approx(5.0)

def test_short_trade_pnl():
    entry_time = datetime(2022, 1, 1, 9, 30)
    exit_time = entry_time + timedelta(hours=6)
    entry_price = 105.0
    exit_price = 100.0
    trade = Trade(entry_time, entry_price, side="short", slippage_pct=0.0)
    trade.close_trade(exit_time, exit_price)
    # For a short trade, profit should equal entry - exit
    assert trade.pnl == pytest.approx(5.0)

def test_trade_slippage():
    entry_time = datetime(2022, 1, 1, 9, 30)
    exit_time = entry_time + timedelta(hours=6)
    entry_price = 100.0
    exit_price = 105.0
    slippage_pct = 0.01  # 1% slippage
    trade = Trade(entry_time, entry_price, side="long", slippage_pct=slippage_pct)
    trade.close_trade(exit_time, exit_price)
    # For long trade, expected exit price is reduced by 1% of exit_price
    expected_exit = exit_price - (slippage_pct * exit_price)
    expected_pnl = expected_exit - entry_price
    assert trade.exit_price == pytest.approx(expected_exit)
    assert trade.pnl == pytest.approx(expected_pnl)

def test_trade_to_dict():
    entry_time = datetime(2022, 1, 1, 9, 30)
    exit_time = entry_time + timedelta(hours=6)
    trade = Trade(entry_time, 100.0, side="long")
    trade.close_trade(exit_time, 105.0)
    trade_dict = trade.to_dict()
    expected_keys = {"entry_time", "entry_price", "exit_time", "exit_price", "side",
                     "capital", "stop_loss", "profit_target", "slippage_pct", "pnl"}
    assert expected_keys.issubset(set(trade_dict.keys()))

if __name__ == "__main__":
    pytest.main()

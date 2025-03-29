# tests/test_strategy.py

import unittest
import pandas as pd
from datetime import datetime, timedelta
from strategies.demark_perfection_strategy import PerfectionStrategy

class TestStrategyLogic(unittest.TestCase):

    def setUp(self):
        # Create fake price data
        dates = pd.date_range(start="2024-01-01", periods=10, freq="D")
        self.price_data = pd.DataFrame({
            "open": [100 + i for i in range(10)],
            "high": [101 + i for i in range(10)],
            "low": [99 + i for i in range(10)],
            "close": [100 + i for i in range(10)],
            "volume": [1000000 for _ in range(10)]
        }, index=dates)

        # Simulated DeMark signal
        self.signal_data = pd.DataFrame({
            "timestamp": [dates[2], dates[5]],
            "symbol": ["AAPL", "AAPL"],
            "signal": ["Perfection9Up", "Perfection9Up"],
            "exchange": ["Cboe-BZX", "Cboe-BZX"],
            "timeframe": ["Daily", "Daily"]
        })

        self.strategy = PerfectionStrategy()

    def test_apply_indicators(self):
        result = self.strategy.apply_indicators(self.price_data.copy())
        self.assertIn("rsi", result.columns)
        self.assertFalse(result["rsi"].isnull().all())  # Should compute actual values

    def test_generate_signals(self):
        signal_df = self.strategy.generate_signals(self.price_data.copy(), self.signal_data)
        self.assertIn("entry_signal", signal_df.columns)
        self.assertTrue((signal_df["entry_signal"] == 1).sum() > 0)  # We expect at least one entry signal

    def test_generate_trades(self):
        signal_df = self.strategy.generate_signals(self.price_data.copy(), self.signal_data)
        trades = self.strategy.generate_trades(signal_df, capital=100000)
        self.assertTrue(len(trades) > 0)
        for trade in trades:
            self.assertIn(trade.side, ["long", "short"])
            self.assertGreater(trade.entry_price, 0)
            self.assertIsNotNone(trade.exit_time)

if __name__ == "__main__":
    unittest.main()

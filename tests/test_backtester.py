# tests/test_backtester.py

import unittest
import pandas as pd
from backtest.backtester import run_backtest
from backtest.trade import Trade
from strategies.demark_perfection_strategy import PerfectionStrategy
from data.data_store import save_df_csv, load_df_csv

class TestBacktester(unittest.TestCase):

    def setUp(self):
        # Create a mock DataFrame of price data
        self.price_data = pd.DataFrame({
            "datetime": pd.date_range(start="2024-01-01", periods=10, freq="D"),
            "open": [100 + i for i in range(10)],
            "high": [101 + i for i in range(10)],
            "low": [99 + i for i in range(10)],
            "close": [100 + i for i in range(10)],
            "volume": [1000] * 10,
        }).set_index("datetime")

        # Create matching signals
        self.signal_data = pd.DataFrame({
            "symbol": ["AAPL"] * 2,
            "signal": ["Perfection9Up", "Perfection9Up"],
            "exchange": ["Cboe-BZX"] * 2,
            "timeframe": ["Daily"] * 2,
            "datetime": [self.price_data.index[2], self.price_data.index[5]]
        })

        # Use a real strategy with simple logic
        self.strategy = PerfectionStrategy()

        self.config = {
            "initial_capital": 10000,
            "slippage_pct": 0.001,
            "side": "long"
        }

    def test_backtest_runs(self):
        results = run_backtest(self.strategy, self.price_data, self.signal_data, self.config)

        self.assertIn("trades", results)
        self.assertIn("metrics", results)
        self.assertIsInstance(results["trades"], list)
        self.assertIsInstance(results["metrics"], dict)

    def test_trade_output_format(self):
        results = run_backtest(self.strategy, self.price_data, self.signal_data, self.config)
        if results["trades"]:
            trade = results["trades"][0]
            self.assertTrue(hasattr(trade, "entry_time"))
            self.assertTrue(hasattr(trade, "exit_time"))
            self.assertTrue(hasattr(trade, "calculate_pnl"))

    def test_metrics_format(self):
        results = run_backtest(self.strategy, self.price_data, self.signal_data, self.config)
        metrics = results["metrics"]
        expected_keys = {"win_rate", "total_return", "max_drawdown", "sharpe_ratio"}
        self.assertTrue(expected_keys.issubset(metrics.keys()))


if __name__ == "__main__":
    unittest.main()

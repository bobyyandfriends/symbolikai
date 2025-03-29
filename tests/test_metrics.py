# tests/test_metrics.py

import unittest
from backtest.trade import Trade
from backtest.metrics import calculate_metrics
from datetime import datetime, timedelta

class TestMetrics(unittest.TestCase):

    def setUp(self):
        # Create sample trades
        self.trades = [
            Trade(
                entry_time=datetime(2024, 1, 1),
                exit_time=datetime(2024, 1, 3),
                entry_price=100,
                exit_price=110,
                side="long",
                capital_allocated=1000,
                signal_strength=1.0
            ),
            Trade(
                entry_time=datetime(2024, 1, 4),
                exit_time=datetime(2024, 1, 6),
                entry_price=200,
                exit_price=180,
                side="short",
                capital_allocated=1000,
                signal_strength=0.9
            )
        ]

        # Apply PnL calculation
        for trade in self.trades:
            trade.calculate_pnl()

    def test_metrics_keys(self):
        metrics = calculate_metrics(self.trades)
        expected_keys = {
            "win_rate", "total_return", "max_drawdown",
            "sharpe_ratio", "profit_factor", "avg_holding_time",
            "exposure"
        }
        self.assertTrue(expected_keys.issubset(metrics.keys()))

    def test_total_return_range(self):
        metrics = calculate_metrics(self.trades)
        self.assertTrue(-1.0 < metrics["total_return"] < 1.0)

    def test_avg_holding_time_format(self):
        metrics = calculate_metrics(self.trades)
        self.assertIsInstance(metrics["avg_holding_time"], float)

    def test_win_rate_calculation(self):
        metrics = calculate_metrics(self.trades)
        self.assertAlmostEqual(metrics["win_rate"], 0.5, delta=0.01)


if __name__ == "__main__":
    unittest.main()

# tests/test_trade.py

import unittest
from datetime import datetime
from backtest.trade import Trade

class TestTrade(unittest.TestCase):

    def setUp(self):
        self.long_trade = Trade(
            entry_time=datetime(2024, 1, 1, 9),
            exit_time=datetime(2024, 1, 2, 15),
            entry_price=100,
            exit_price=110,
            side="long",
            capital_allocated=1000,
            signal_strength=0.9
        )

        self.short_trade = Trade(
            entry_time=datetime(2024, 1, 3, 10),
            exit_time=datetime(2024, 1, 4, 14),
            entry_price=150,
            exit_price=140,
            side="short",
            capital_allocated=1500,
            signal_strength=0.7
        )

    def test_calculate_pnl_long(self):
        self.long_trade.calculate_pnl()
        expected_pnl = (110 - 100) / 100 * 1000
        self.assertAlmostEqual(self.long_trade.pnl, expected_pnl, delta=0.01)

    def test_calculate_pnl_short(self):
        self.short_trade.calculate_pnl()
        expected_pnl = (150 - 140) / 150 * 1500
        self.assertAlmostEqual(self.short_trade.pnl, expected_pnl, delta=0.01)

    def test_apply_slippage(self):
        self.long_trade.apply_slippage(slippage_pct=0.01)
        self.assertAlmostEqual(self.long_trade.entry_price, 101.0)
        self.assertAlmostEqual(self.long_trade.exit_price, 108.9)

    def test_to_dict(self):
        self.long_trade.calculate_pnl()
        trade_dict = self.long_trade.to_dict()
        self.assertIsInstance(trade_dict, dict)
        self.assertIn("entry_price", trade_dict)
        self.assertIn("exit_price", trade_dict)
        self.assertIn("pnl", trade_dict)


if __name__ == "__main__":
    unittest.main()

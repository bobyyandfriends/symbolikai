# tests/test_ml.py

import unittest
import pandas as pd
from ml.environment_classifier import classify_environment
from ml.self_reflection import generate_commentary
from datetime import datetime

class TestMLComponents(unittest.TestCase):

    def setUp(self):
        self.sample_trades = pd.DataFrame([
            {"entry_time": datetime(2024, 1, 1), "exit_time": datetime(2024, 1, 2), "pnl": 150, "signal_strength": 0.9, "features": {"rsi": 45}},
            {"entry_time": datetime(2024, 1, 3), "exit_time": datetime(2024, 1, 5), "pnl": -80, "signal_strength": 0.6, "features": {"rsi": 72}},
            {"entry_time": datetime(2024, 1, 6), "exit_time": datetime(2024, 1, 7), "pnl": 20, "signal_strength": 0.4, "features": {"rsi": 30}},
        ])

    def test_environment_classifier(self):
        labels = classify_environment(self.sample_trades)
        self.assertEqual(len(labels), len(self.sample_trades))
        self.assertTrue(set(labels).issubset({"bull", "bear", "neutral"}))

    def test_generate_commentary(self):
        trade = self.sample_trades.iloc[1].to_dict()
        comment = generate_commentary(trade)
        self.assertIsInstance(comment, str)
        self.assertGreater(len(comment), 0)
        self.assertIn("signal_strength", comment.lower())  # should refer to factors

if __name__ == "__main__":
    unittest.main()

# tests/test_data.py

import unittest
import pandas as pd
import os
from data.data_store import save_df_csv, load_df_csv
from data.signal_loader import normalize_signals, deduplicate_signals
from datetime import datetime
from tempfile import TemporaryDirectory


class TestDataOperations(unittest.TestCase):

    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.test_file_path = os.path.join(self.temp_dir.name, "test_data.csv")

        self.sample_df = pd.DataFrame({
            "symbol": ["AAPL", "AAPL"],
            "signal": ["C13Up", "C13Up"],
            "exchange": ["Cboe-BZX", "Cboe-BZX"],
            "timeframe": ["Daily", "Daily"],
            "timestamp": [pd.Timestamp("2024-01-01 09:30"), pd.Timestamp("2024-01-01 09:30")]
        })

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_save_and_load_csv(self):
        save_df_csv(self.sample_df, self.test_file_path)
        loaded_df = load_df_csv(self.test_file_path)
        pd.testing.assert_frame_equal(self.sample_df, loaded_df)

    def test_normalize_signals(self):
        raw_df = pd.DataFrame({
            "Symbol": ["AAPL"],
            "Signal1": [" C13Up "],
            "Exchange": ["Cboe-BZX"],
            "Timeframe": ["Daily"],
            "Date": ["Jan 01, 2024 09:30"]
        })

        norm_df = normalize_signals(raw_df)
        self.assertEqual(norm_df.columns.tolist(), ["symbol", "signal", "exchange", "timeframe", "timestamp"])
        self.assertEqual(norm_df.iloc[0]["signal"], "C13Up")
        self.assertIsInstance(norm_df.iloc[0]["timestamp"], pd.Timestamp)

    def test_deduplicate_signals(self):
        new_df = self.sample_df.copy()
        combined = deduplicate_signals(existing_df=self.sample_df, new_df=new_df)
        self.assertEqual(len(combined), 1)  # Duplicate should be removed


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
import pandas as pd
from typing import List, Dict
import json
import os

class TradeReflection:
    """
    Provides post-trade analysis and self-reflection commentary for ML trades.
    Labels trades (good, okay, bad) based on trade performance and surfaces lessons.
    """
    def __init__(self, save_path: str = "ml/reflection_logs/"):
        self.save_path = save_path
        # Ensure the save_path directory exists.
        os.makedirs(self.save_path, exist_ok=True)

    def label_trade_quality(self, trade: dict) -> str:
        """
        Classify trade quality as "good", "okay", or "bad".
        Here, pnl is used as the primary measure; you can adjust thresholds as needed.
        For example, a profit (pnl) above 0.02 is "good", positive but lower is "okay", else "bad".
        """
        pnl = trade.get("pnl", 0)
        # Custom thresholds; these can be adjusted to your risk/reward preferences.
        if pnl > 0.02:
            return "good"
        elif pnl > 0:
            return "okay"
        else:
            return "bad"

    def reflect_on_trade(self, trade: dict, model_features: Dict[str, float]) -> str:
        """
        Generate commentary for a trade based on its outcome and provided model features.
        
        Parameters:
          trade: Dictionary with trade details (including "pnl").
          model_features: Dictionary of feature values for the trade context (e.g., rsi, volatility).
          
        Returns:
          A string containing a quality label and insights.
        """
        quality = self.label_trade_quality(trade)
        comments = []

        if quality == "good":
            comments.append("Trade met or exceeded profit expectations.")
            if model_features.get("volatility", 0) > 0.02:
                comments.append("Model correctly handled high volatility.")
        elif quality == "bad":
            comments.append("Trade failed to reach target.")
            if model_features.get("rsi", 50) > 70:
                comments.append("Consider avoiding overbought entries.")
            if model_features.get("momentum", 0) < 0:
                comments.append("Momentum may have been misaligned.")
        else:  # "okay"
            comments.append("Trade had modest gain.")
            comments.append("Review risk/reward ratio for optimization.")

        return f"Quality: {quality.upper()} | Insights: {' '.join(comments)}"

    def evaluate_batch(self, trades: List[dict], feature_lookup: Dict[str, Dict], run_id: str) -> List[dict]:
        """
        Process a batch of trades and generate a full reflection log.
        
        For each trade, it looks up model features based on a trade identifier (constructed using symbol and entry time),
        generates a quality label and reflection commentary, and then saves the log to a JSON file.
        
        Parameters:
          trades: List of trade dictionaries. Each trade should contain at least "symbol", "entry_time", and "pnl".
          feature_lookup: Dictionary mapping trade IDs (e.g., "AAPL_2022-01-01 00:00:00") to feature dictionaries.
          run_id: Identifier for the current batch run (used in the filename).
          
        Returns:
          A list of trade dictionaries augmented with "quality" and "reflection" fields.
        """
        log = []
        for trade in trades:
            symbol = trade.get("symbol", "UNKNOWN")
            entry_time = str(trade.get("entry_time"))
            # Create a trade identifier; adjust format as needed.
            trade_id = f"{symbol}_{entry_time}"
            features = feature_lookup.get(trade_id, {})

            reflection = self.reflect_on_trade(trade, features)
            trade["quality"] = self.label_trade_quality(trade)
            trade["reflection"] = reflection
            log.append(trade)

        log_filename = os.path.join(self.save_path, f"reflection_{run_id}.json")
        with open(log_filename, "w") as f:
            json.dump(log, f, indent=2)
        print(f"Reflection log saved to: {log_filename}")

        return log

if __name__ == "__main__":
    # Example usage:
    from datetime import datetime, timedelta
    # Dummy trade data
    trades = [
        {
            "symbol": "AAPL",
            "entry_time": datetime(2022, 1, 1).isoformat(),
            "exit_time": (datetime(2022, 1, 5)).isoformat(),
            "pnl": 0.03
        },
        {
            "symbol": "AAPL",
            "entry_time": datetime(2022, 1, 10).isoformat(),
            "exit_time": (datetime(2022, 1, 15)).isoformat(),
            "pnl": 0.01
        },
        {
            "symbol": "AAPL",
            "entry_time": datetime(2022, 1, 20).isoformat(),
            "exit_time": (datetime(2022, 1, 25)).isoformat(),
            "pnl": -0.02
        }
    ]
    # Dummy feature lookup (keys should match trade_id format: "AAPL_<entry_time>")
    feature_lookup = {
        f"AAPL_{datetime(2022, 1, 1).isoformat()}": {"rsi": 28, "volatility": 0.03, "momentum": 1.2},
        f"AAPL_{datetime(2022, 1, 10).isoformat()}": {"rsi": 40, "volatility": 0.015, "momentum": 0.8},
        f"AAPL_{datetime(2022, 1, 20).isoformat()}": {"rsi": 75, "volatility": 0.025, "momentum": -0.5}
    }
    
    reflection = TradeReflection()
    # Using a dummy run_id for the log filename.
    log = reflection.evaluate_batch(trades, feature_lookup, run_id="test_run")
    print("Reflection Log Sample:")
    for entry in log:
        print(entry)

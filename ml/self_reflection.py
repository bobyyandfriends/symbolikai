# ml/self_reflection.py

import pandas as pd
from typing import List, Dict
import random
import json


class TradeReflection:
    """
    Provides post-trade analysis and self-reflection commentary for ML trades.
    Labels good/bad trades and surfaces lessons.
    """

    def __init__(self, save_path="ml/reflection_logs/"):
        self.save_path = save_path

    def label_trade_quality(self, trade: dict) -> str:
        """
        Classify trade quality (good, okay, bad) based on return, duration, or custom thresholds.
        """
        pnl = trade["pnl"]
        duration = trade.get("duration", 0)
        if pnl > 0.02:
            return "good"
        elif pnl > 0:
            return "okay"
        else:
            return "bad"

    def reflect_on_trade(self, trade: dict, model_features: Dict[str, float]) -> str:
        """
        Generate commentary about a trade based on its outcome and input features.
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
        else:
            comments.append("Trade had modest gain.")
            comments.append("Review risk/reward ratio for optimization.")

        return f"Quality: {quality.upper()} | Insights: {' '.join(comments)}"

    def evaluate_batch(self, trades: List[dict], feature_lookup: Dict[str, Dict], run_id: str):
        """
        Process a batch of trades and generate full reflection log.
        Each trade gets a quality score and comments.
        """
        log = []
        for trade in trades:
            symbol = trade["symbol"]
            entry_time = str(trade["entry_time"])
            trade_id = f"{symbol}_{entry_time}"
            features = feature_lookup.get(trade_id, {})

            reflection = self.reflect_on_trade(trade, features)
            trade["quality"] = self.label_trade_quality(trade)
            trade["reflection"] = reflection
            log.append(trade)

        with open(f"{self.save_path}/reflection_{run_id}.json", "w") as f:
            json.dump(log, f, indent=2)

        return log

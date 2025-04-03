#!/usr/bin/env python3
"""
self_reflection.py

Enhanced version of TradeReflection to:
  - Label trades 'good', 'okay', or 'bad' based on PnL
  - Optionally incorporate synergy or Kelly fraction in the reflection commentary
  - Produce batch-level stats for synergy usage, e.g. average synergy among winners
  - Save reflections to JSON for record-keeping

Usage Steps:
  1) Provide a list of trade dicts, each with at least 'symbol','entry_time','pnl'.
  2) Optionally have 'synergy_score','kelly_fraction' in each trade if synergy or Kelly used.
  3) Provide a feature_lookup dict if you want to incorporate advanced feature references in reflection.

Example:
   reflection = TradeReflection()
   final_log = reflection.evaluate_batch(trades, feature_lookup, run_id="session_001")
"""

import os
import json
import pandas as pd
import numpy as np
from typing import List, Dict, Union


class TradeReflection:
    """
    Provides post-trade analysis and reflection commentary for ML trades.
    - Classifies trade quality: good/okay/bad
    - Generates insights factoring synergy or kelly fraction if present
    - Writes reflection logs to JSON
    """

    def __init__(self,
                 save_path: str = "ml/reflection_logs/",
                 good_threshold: float = 0.02,
                 okay_threshold: float = 0.0,
                 synergy_threshold: float = 2.0):
        """
        :param save_path: Directory to save reflection logs as JSON
        :param good_threshold: If PnL > this, trade is 'good'
        :param okay_threshold: If PnL > okay_threshold but <= good_threshold => 'okay'
                               else 'bad' if below okay_threshold
        :param synergy_threshold: synergy reference for commentary, if synergy is used
        """
        self.save_path = save_path
        os.makedirs(self.save_path, exist_ok=True)

        self.good_threshold = good_threshold
        self.okay_threshold = okay_threshold
        self.synergy_threshold = synergy_threshold

    def label_trade_quality(self, trade: dict) -> str:
        """
        Classify trade quality as "good", "okay", or "bad" based on trade's 'pnl'.
        Uses thresholds:
           - > good_threshold => 'good'
           - > okay_threshold => 'okay'
           - else => 'bad'
        """
        pnl = trade.get("pnl", 0.0)

        if pnl > self.good_threshold:
            return "good"
        elif pnl > self.okay_threshold:
            return "okay"
        else:
            return "bad"

    def reflect_on_trade(self, trade: dict, features: dict = None) -> str:
        """
        Generate a reflection commentary for a single trade.
        Incorporates synergy, kelly_fraction, or feature references if present.

        :param trade: single trade dict, e.g. 
               {
                 'symbol': 'AAPL',
                 'entry_time': '2023-01-01T09:30:00',
                 'pnl': 0.025,
                 'synergy_score': 2.5,
                 'kelly_fraction': 0.15,
                 ...
               }
        :param features: optional dict of feature values for the trade, e.g. { 'rsi':72, ... }
        :return: textual commentary
        """
        quality = self.label_trade_quality(trade)
        synergy = trade.get("synergy_score")
        kelly = trade.get("kelly_fraction")
        commentary_lines = []

        # Basic outcome line
        commentary_lines.append(f"Trade was labeled {quality.upper()} with PnL {trade.get('pnl',0.0):.4f}.")

        # synergy mention
        if synergy is not None:
            if synergy >= self.synergy_threshold:
                commentary_lines.append(f"Synergy was strong ({synergy:.2f}), supporting the entry.")
            else:
                commentary_lines.append(f"Synergy was moderate/low ({synergy:.2f}).")

        # Kelly mention
        if kelly is not None:
            commentary_lines.append(f"Kelly fraction used: {kelly:.2f}. Consider adjusting if max drawdowns are high.")

        # If we want advanced feature references
        if features is not None and len(features) > 0:
            # e.g. if rsi > 70 => mention
            rsi_val = features.get("rsi", None)
            if rsi_val is not None:
                if rsi_val > 70:
                    commentary_lines.append("Note: RSI was high at entry, risking an overbought scenario.")
                elif rsi_val < 30:
                    commentary_lines.append("RSI was low at entry, a contrarian approach that can yield bigger rebounds.")

        # finalize
        reflection_text = " ".join(commentary_lines)
        return reflection_text

    def evaluate_batch(self,
                       trades: List[dict],
                       feature_lookup: Dict[str, dict] = None,
                       run_id: str = "default_run") -> List[dict]:
        """
        Reflect on a batch of trades. For each trade:
         1) label trade quality
         2) generate reflection commentary
         3) store results in final log

        Then write the log to a JSON file named reflection_<run_id>.json

        Also produce summary stats:
         - distribution of good/okay/bad
         - synergy-based stats if synergy is used

        :param trades: list of trade dicts
        :param feature_lookup: optional mapping from trade_id => {features}
                               trade_id can be symbol + entry_time or any unique key
        :param run_id: used in the output filename
        :return: the augmented trades with 'quality' and 'reflection' fields
        """
        if feature_lookup is None:
            feature_lookup = {}

        for trade in trades:
            symbol = trade.get("symbol","UNKNOWN")
            entry_time = str(trade.get("entry_time",""))
            # create a trade_id to match feature_lookup
            trade_id = f"{symbol}_{entry_time}"
            features = feature_lookup.get(trade_id, {})

            q = self.label_trade_quality(trade)
            reflection = self.reflect_on_trade(trade, features)
            trade["quality"] = q
            trade["reflection"] = reflection

        # Summaries
        df_trades = pd.DataFrame(trades)
        total = len(df_trades)
        if total == 0:
            print("[TradeReflection] No trades to reflect on.")
            return trades

        # distribution of quality
        counts = df_trades['quality'].value_counts()
        print("[TradeReflection] Quality distribution:")
        for cat, cnt in counts.items():
            print(f"  {cat}: {cnt} trades => {cnt/total*100:.1f}%")

        # synergy-based stats if synergy_score is present
        if 'synergy_score' in df_trades.columns:
            synergy_winners = df_trades[(df_trades['quality']=='good') & (df_trades['synergy_score'].notna())]
            synergy_losers = df_trades[(df_trades['quality']=='bad') & (df_trades['synergy_score'].notna())]
            if not synergy_winners.empty:
                avg_synergy_win = synergy_winners['synergy_score'].mean()
                print(f"  Average synergy of 'good' trades: {avg_synergy_win:.2f}")
            if not synergy_losers.empty:
                avg_synergy_bad = synergy_losers['synergy_score'].mean()
                print(f"  Average synergy of 'bad' trades: {avg_synergy_bad:.2f}")

        # Save the reflection log
        out_log = os.path.join(self.save_path, f"reflection_{run_id}.json")
        with open(out_log, "w") as f:
            json.dump(trades, f, indent=2, default=str)
        print(f"[TradeReflection] Reflection log saved to: {out_log}")

        return trades


if __name__ == "__main__":
    # demonstration
    from datetime import datetime
    # sample trades
    trades_example = [
        {
            "symbol": "AAPL",
            "entry_time": datetime(2023,1,1,9,30).isoformat(),
            "exit_time": datetime(2023,1,5,16,0).isoformat(),
            "pnl": 0.03,
            "synergy_score": 2.3,
            "kelly_fraction": 0.10
        },
        {
            "symbol": "AAPL",
            "entry_time": datetime(2023,1,7,9,30).isoformat(),
            "exit_time": datetime(2023,1,10,16,0).isoformat(),
            "pnl": 0.005
        },
        {
            "symbol": "AAPL",
            "entry_time": datetime(2023,1,12,9,30).isoformat(),
            "exit_time": datetime(2023,1,15,16,0).isoformat(),
            "pnl": -0.01,
            "synergy_score": 1.2
        }
    ]

    # optional feature lookup
    feature_lookup_demo = {
        "AAPL_2023-01-01T09:30:00": {"rsi":72, "volatility":0.03},
        "AAPL_2023-01-07T09:30:00": {"rsi":45},
        "AAPL_2023-01-12T09:30:00": {"rsi":28}
    }

    reflection = TradeReflection(save_path="ml/reflection_logs/",
                                 good_threshold=0.02, 
                                 okay_threshold=0.0,
                                 synergy_threshold=2.0)

    final_log = reflection.evaluate_batch(trades_example, feature_lookup_demo, run_id="example_run")
    print("[Demo] Reflection results:")
    for t in final_log:
        print(f"- {t['symbol']} {t['entry_time']} => quality={t['quality']} => reflection={t['reflection']}")

# strategies/demark_perfection_strategy.py

import pandas as pd
import pandas_ta as ta
from strategies.base_strategy import Strategy
from strategies.rule_engine import evaluate_rule

class Perfection9UpStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.name = "Perfection9UpStrategy"

    def apply_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        df["RSI"] = ta.rsi(df["close"], length=14)
        return df

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        rule = [
            {"col": "signal_type", "op": "==", "val": "Perfection9Up"},
            {"col": "RSI", "op": "<", "val": 60},
        ]
        df["entry"] = evaluate_rule(df, rule)
        return df

    def generate_trades(self, df: pd.DataFrame) -> pd.DataFrame:
        trades = []

        for i in range(len(df)):
            if df["entry"].iloc[i]:
                entry_price = df["close"].iloc[i]
                entry_time = df.index[i]

                # Exit 5 bars later or earlier if stop-loss hit
                exit_index = i + 5 if i + 5 < len(df) else len(df) - 1
                exit_price = df["close"].iloc[exit_index]
                exit_time = df.index[exit_index]

                trade = {
                    "entry_time": entry_time,
                    "exit_time": exit_time,
                    "entry_price": entry_price,
                    "exit_price": exit_price,
                    "side": "long",
                    "signal": "Perfection9Up",
                }
                trades.append(trade)

        return pd.DataFrame(trades)

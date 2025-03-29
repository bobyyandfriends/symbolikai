# strategies/combo_strategy_example.py

import pandas as pd
from strategies.base_strategy import BaseStrategy
from strategies.rule_engine import evaluate_rule
import pandas_ta as ta

class ComboStrategy(BaseStrategy):
    """
    Strategy that combines multiple DeMark signals with indicator filters
    for refined entry/exit decisions. Supports long and short logic.
    """

    def __init__(self):
        super().__init__(name="ComboStrategy")

    def apply_indicators(self, price_data: pd.DataFrame) -> pd.DataFrame:
        df = price_data.copy()
        df["rsi"] = ta.rsi(df["close"], length=14)
        df["momentum"] = ta.mom(df["close"], length=10)
        df["ema_21"] = ta.ema(df["close"], length=21)
        return df

    def generate_signals(self, df: pd.DataFrame, signal_data: pd.DataFrame) -> pd.DataFrame:
        """
        Combine multiple DeMark signals and indicator filters to produce entry signals.
        """
        df = self.apply_indicators(df)

        # Merge signal data onto price data
        signal_matrix = pd.pivot_table(
            signal_data, index="datetime", columns="signal", values="signal", aggfunc=lambda x: True
        ).fillna(False)

        combined = df.join(signal_matrix, how="left").fillna(False)

        # Example long entry logic
        combined["long_entry"] = (
            (combined["C13Up"]) &
            (combined["Perfection9Up"]) &
            (combined["rsi"] < 50) &
            (combined["momentum"] > 0)
        )

        # Example short entry logic
        combined["short_entry"] = (
            (combined["C13Down"]) &
            (combined["Perfection9Down"]) &
            (combined["rsi"] > 50) &
            (combined["momentum"] < 0)
        )

        return combined

    def generate_trades(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Convert entry/exit signals into trade records.
        """
        trades = []
        position = None

        for i in range(len(df)):
            row = df.iloc[i]
            time = df.index[i]
            price = row["close"]

            # Open new long position
            if position is None and row["long_entry"]:
                position = {
                    "side": "long",
                    "entry_time": time,
                    "entry_price": price,
                }

            # Open new short position
            elif position is None and row["short_entry"]:
                position = {
                    "side": "short",
                    "entry_time": time,
                    "entry_price": price,
                }

            # Exit long position
            elif position and position["side"] == "long" and (row["rsi"] > 70 or row["momentum"] < 0):
                position.update({
                    "exit_time": time,
                    "exit_price": price
                })
                trades.append(position)
                position = None

            # Exit short position
            elif position and position["side"] == "short" and (row["rsi"] < 30 or row["momentum"] > 0):
                position.update({
                    "exit_time": time,
                    "exit_price": price
                })
                trades.append(position)
                position = None

        return trades

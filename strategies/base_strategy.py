# strategies/base_strategy.py

import pandas as pd
from abc import ABC, abstractmethod
from typing import List, Dict

class Strategy(ABC):
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.indicators_enabled = True

    @abstractmethod
    def generate_signals(self, price_data: pd.DataFrame, signal_data: pd.DataFrame) -> pd.DataFrame:
        """
        Must return a DataFrame with 'entry' and 'exit' signals as boolean columns.
        """
        pass

    def apply_indicators(self, price_data: pd.DataFrame) -> pd.DataFrame:
        """
        Optional: Override to apply technical indicators like RSI, Momentum, etc.
        """
        return price_data

    def generate_trades(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Uses signal columns ('entry' and 'exit') to generate a trade list.
        Can be extended or customized by subclasses.
        """
        df = df.copy()
        df["position"] = 0  # 1 = long, -1 = short

        in_trade = False
        for i in range(len(df)):
            if not in_trade and df.at[i, "entry"]:
                df.at[i, "position"] = 1
                in_trade = True
            elif in_trade and df.at[i, "exit"]:
                df.at[i, "position"] = 0
                in_trade = False
            else:
                df.at[i, "position"] = df.at[i-1, "position"] if i > 0 else 0

        return df

    def get_name(self):
        return self.__class__.__name__

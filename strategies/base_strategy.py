#!/usr/bin/env python3
from abc import ABC, abstractmethod
import pandas as pd

class Strategy(ABC):
    """
    Abstract base class for all trading strategies.
    Custom strategies must implement the methods defined below.
    """

    def __init__(self, name: str = "BaseStrategy", **kwargs):
        """
        Initialize the strategy with a name and optional parameters.
        """
        self.name = name
        self.params = kwargs

    @abstractmethod
    def generate_signals(self, price_data: pd.DataFrame, signal_data: pd.DataFrame) -> pd.DataFrame:
        """
        Analyze price and signal data to generate entry and exit signals.
        Should return a DataFrame containing at least a 'timestamp' column and a 'signal' column.
        """
        pass

    @abstractmethod
    def apply_indicators(self, price_data: pd.DataFrame) -> pd.DataFrame:
        """
        Compute technical indicators (e.g. RSI, EMA, etc.) on the price data.
        Returns a DataFrame with additional indicator columns.
        """
        pass

    @abstractmethod
    def generate_trades(self, price_data: pd.DataFrame, signals: pd.DataFrame) -> pd.DataFrame:
        """
        Convert the generated signals into a trade log.
        Should return a DataFrame that includes trade details such as entry time, exit time, prices, etc.
        """
        pass

    def __str__(self):
        return f"{self.name} Strategy with parameters: {self.params}"


# The following test code is optional.
# It lets you run this file as a script to verify that it can be imported without errors.
if __name__ == "__main__":
    # Since Strategy is abstract, attempting to instantiate it directly will raise an error.
    # This block is only for demonstration purposes.
    try:
        s = Strategy()
    except TypeError as e:
        print("Cannot instantiate abstract class Strategy:", e)

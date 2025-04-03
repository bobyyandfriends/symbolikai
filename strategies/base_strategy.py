#!/usr/bin/env python3
"""
base_strategy.py

Defines a generic BaseStrategy class for SymbolikAI. 
Child strategy classes should override generate_signals() and generate_trades()
with the actual logic. This base includes synergy references and placeholders
for pivot or fundamental usage.
"""

import pandas as pd

class BaseStrategy:
    """
    A base class that other strategies can inherit.

    Typical usage:
      1. Subclass and implement generate_signals(price_data) to produce a DataFrame
         or series of signal events (buy, sell, synergy_info, pivot_flags, etc.).
      2. Or skip that, and go straight to generate_trades(...) if your logic
         directly outputs trades.

    The synergy approach:
      - If you want synergy at the strategy level, you can define synergy
        aggregator logic here. Or have child classes produce synergy.

    The idea is to keep a consistent interface for the backtester:
      - backtester calls strategy.generate_trades(price_data, signals)
        and expects a DataFrame of trades with columns like:
          [entry_time, exit_time, side, entry_price, exit_price, synergy_score, commentary, ...]

    You might unify synergy logic either in a synergy aggregator or within each strategy.
    """

    def __init__(self, name="BaseStrategy", config=None):
        """
        :param name: string name
        :param config: a dict or object with config parameters
        """
        if config is None:
            config = {}
        self.name = name
        self.config = config

    def generate_signals(self, price_data: pd.DataFrame) -> pd.DataFrame:
        """
        Optional method that produces intermediate signals from the price_data.
        For example, hooking in pivot detection, demark signals, synergy alignment, etc.

        By default, we do nothing. Child classes can override.
        :param price_data: DataFrame with columns like 'datetime','open','high','low','close','volume'
        :return: DataFrame or Series of signals (with times). Could have columns:
                 e.g. 'datetime','demark_signal','pivot_signal','synergy_signal'
        """
        # Placeholder no-op
        df_signals = pd.DataFrame()
        return df_signals

    def generate_trades(self, price_data: pd.DataFrame,
                        signal_data: pd.DataFrame = None) -> pd.DataFrame:
        """
        Produce final trade objects or rows from price_data plus signals.
        Typically returns a DataFrame with columns:
          - entry_time
          - exit_time
          - entry_price
          - exit_price
          - side (long/short)
          - synergy_score (optional)
          - reason_codes
          - commentary
          - quantity
          - profit (optionally)
        :param price_data: DataFrame
        :param signal_data: DataFrame of signals or synergy references
        :return: DataFrame of trades (one row per trade)
        """
        # Child classes should override this method with actual logic.
        # This is a dummy placeholder to illustrate the structure.
        trades_list = []

        # For demonstration, we do a trivial example: no trades
        # Insert your logic or override in child classes
        trades_df = pd.DataFrame(trades_list, columns=[
            'entry_time', 'exit_time',
            'entry_price', 'exit_price',
            'side', 'synergy_score',
            'reason_codes', 'commentary',
            'quantity', 'profit'
        ])
        return trades_df


# Example usage or testing
if __name__ == "__main__":
    # We'll show how a child strategy might override the base
    class ExampleStrategy(BaseStrategy):
        def generate_signals(self, price_data: pd.DataFrame) -> pd.DataFrame:
            # e.g. produce a dummy synergy signal for each row
            df_signals = price_data.copy()
            df_signals['datetime'] = df_signals.index if 'datetime' not in df_signals.columns else df_signals['datetime']
            df_signals['synergy_signal'] = 1  # placeholder
            return df_signals

        def generate_trades(self, price_data: pd.DataFrame, signal_data: pd.DataFrame = None) -> pd.DataFrame:
            if signal_data is None or signal_data.empty:
                return pd.DataFrame()  # no trades

            # A trivial "once off" trade example
            # Suppose we buy on the first row of signals
            first_row = signal_data.iloc[0]
            last_row = signal_data.iloc[-1]
            trades_list = [{
                'entry_time': first_row['datetime'],
                'entry_price': first_row['close'],
                'exit_time': last_row['datetime'],
                'exit_price': last_row['close'],
                'side': 'long',
                'synergy_score': 2.0,
                'reason_codes': 'Demo',
                'commentary': 'Dummy trade from first to last bar',
                'quantity': 10,
                'profit': (last_row['close'] - first_row['close']) * 10
            }]
            trades_df = pd.DataFrame(trades_list)
            return trades_df

    # Quick demo
    import numpy as np

    # Fake price data
    idx = pd.date_range("2023-01-01", periods=5, freq="D")
    close_prices = np.array([100, 101, 102, 101, 103])
    df_price = pd.DataFrame({'close': close_prices}, index=idx)

    # Instantiate example strategy
    strat = ExampleStrategy(name="Example")
    # generate signals
    signals = strat.generate_signals(df_price)
    print("Signals:\n", signals)
    # generate trades
    trades = strat.generate_trades(df_price, signals)
    print("\nTrades:\n", trades)

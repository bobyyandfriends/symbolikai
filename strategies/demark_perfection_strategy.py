#!/usr/bin/env python3
import pandas as pd
import numpy as np
import os
import sys

# Dynamically add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from strategies.base_strategy import BaseStrategy

class DemarkPerfectionStrategy(BaseStrategy):
    """
    A strategy that uses a 'Perfection9Up' concept.
    It calculates RSI and SMA, and marks a buy signal ('buy_perfection9up') when RSI is low and a local minimum is detected.
    A sell signal is generated when RSI rises above a threshold or the price moves above the SMA.
    """
    def __init__(self, rsi_period: int = 14, sma_period: int = 50, perfection_rsi_threshold: float = 35, **kwargs):
        super().__init__(name="DemarkPerfectionStrategy", **kwargs)
        self.rsi_period = rsi_period
        self.sma_period = sma_period
        self.perfection_rsi_threshold = perfection_rsi_threshold

    def apply_indicators(self, price_data: pd.DataFrame) -> pd.DataFrame:
        df = price_data.copy().sort_values('datetime').reset_index(drop=True)
        delta = df['close'].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(window=self.rsi_period, min_periods=self.rsi_period).mean()
        avg_loss = loss.rolling(window=self.rsi_period, min_periods=self.rsi_period).mean()
        rs = avg_gain / (avg_loss + 1e-10)
        df['rsi'] = 100 - (100 / (1 + rs))
        df['sma'] = df['close'].rolling(window=self.sma_period, min_periods=self.sma_period).mean()
        # Identify local minima: mark as True if the low is lower than the previous two bars
        df['is_local_min'] = (df['low'] < df['low'].shift(1)) & (df['low'] < df['low'].shift(2))
        return df

    def generate_signals(self, price_data: pd.DataFrame, signal_data: pd.DataFrame = None) -> pd.DataFrame:
        df = self.apply_indicators(price_data)
        df = df.dropna(subset=['rsi', 'sma']).copy()
        df['signal'] = None

        # Generate a buy signal when RSI is below the perfection threshold and a local minimum occurs.
        buy_condition = (df['rsi'] < self.perfection_rsi_threshold) & (df['is_local_min'])
        df.loc[buy_condition, 'signal'] = 'buy_perfection9up'
        
        # Generate a sell signal when RSI rises above 65 or price moves above SMA.
        sell_condition = (df['rsi'] > 65) | (df['close'] > df['sma'])
        df.loc[sell_condition, 'signal'] = 'sell'
        
        signals = df[['datetime', 'signal']].dropna().reset_index(drop=True)
        return signals

    def generate_trades(self, price_data: pd.DataFrame, signals: pd.DataFrame) -> pd.DataFrame:
        price_df = price_data.sort_values('datetime').reset_index(drop=True)
        signals = signals.sort_values('datetime').reset_index(drop=True)
        trades = []
        in_position = False
        entry_time, entry_price = None, None

        for idx, row in signals.iterrows():
            signal_time = row['datetime']
            signal_type = row['signal']
            current_row = price_df[price_df['datetime'] >= signal_time].iloc[0]
            current_price = current_row['close']

            if signal_type == 'buy_perfection9up' and not in_position:
                in_position = True
                entry_time = current_row['datetime']
                entry_price = current_price
            elif signal_type == 'sell' and in_position:
                exit_time = current_row['datetime']
                exit_price = current_price
                profit = exit_price - entry_price
                trades.append({
                    'entry_time': entry_time,
                    'entry_price': entry_price,
                    'exit_time': exit_time,
                    'exit_price': exit_price,
                    'profit': profit
                })
                in_position = False
                entry_time, entry_price = None, None

        if in_position:
            last_row = price_df.iloc[-1]
            trades.append({
                'entry_time': entry_time,
                'entry_price': entry_price,
                'exit_time': last_row['datetime'],
                'exit_price': last_row['close'],
                'profit': last_row['close'] - entry_price
            })

        return pd.DataFrame(trades)

if __name__ == "__main__":
    # Example usage with dummy data:
    dates = pd.date_range(start="2022-01-01", periods=100, freq='D')
    np.random.seed(42)
    prices = np.cumsum(np.random.randn(100)) + 100
    volume = np.random.randint(100, 1000, size=100)
    price_data = pd.DataFrame({
        'datetime': dates,
        'open': prices + np.random.randn(100)*0.5,
        'high': prices + np.random.rand(100),
        'low': prices - np.random.rand(100),
        'close': prices,
        'volume': volume
    })

    strategy = DemarkPerfectionStrategy()
    signals = strategy.generate_signals(price_data)
    print("Generated Signals:")
    print(signals.head())
    trades = strategy.generate_trades(price_data, signals)
    print("\nSimulated Trades:")
    print(trades.head())

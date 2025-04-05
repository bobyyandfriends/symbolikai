#!/usr/bin/env python3
import pandas as pd
import numpy as np
import os
import sys

# Dynamically add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from strategies.base_strategy import BaseStrategy

class ComboStrategyExample(BaseStrategy):
    """
    Example strategy that combines multiple signals:
    - A simulated C13Up signal, defined here as the condition when the closing price is above a short-term SMA.
    - A momentum filter: current close minus previous close > 0.
    - An RSI filter: RSI is below a specified threshold.
    """
    def __init__(self, sma_period: int = 20, rsi_period: int = 14, momentum_threshold: float = 0,
                 rsi_filter: float = 40, **kwargs):
        super().__init__(name="ComboStrategyExample", **kwargs)
        self.sma_period = sma_period
        self.rsi_period = rsi_period
        self.momentum_threshold = momentum_threshold
        self.rsi_filter = rsi_filter

    def apply_indicators(self, price_data: pd.DataFrame) -> pd.DataFrame:
        df = price_data.copy().sort_values('datetime').reset_index(drop=True)
        # Calculate short-term SMA as a proxy for C13Up signal
        df['sma'] = df['close'].rolling(window=self.sma_period, min_periods=self.sma_period).mean()

        # Calculate RSI
        delta = df['close'].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(window=self.rsi_period, min_periods=self.rsi_period).mean()
        avg_loss = loss.rolling(window=self.rsi_period, min_periods=self.rsi_period).mean()
        rs = avg_gain / (avg_loss + 1e-10)
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # Calculate momentum (difference between current and previous close)
        df['momentum'] = df['close'] - df['close'].shift(1)
        
        # Simulate a C13Up condition: true when close is above the SMA
        df['c13up'] = df['close'] > df['sma']
        return df

    def generate_signals(self, price_data: pd.DataFrame, signal_data: pd.DataFrame = None) -> pd.DataFrame:
        df = self.apply_indicators(price_data)
        df = df.dropna(subset=['sma', 'rsi', 'momentum']).copy()
        df['signal'] = None

        # Buy signal: when C13Up condition is true, momentum is positive, and RSI is below the threshold.
        buy_condition = (df['c13up']) & (df['momentum'] > self.momentum_threshold) & (df['rsi'] < self.rsi_filter)
        df.loc[buy_condition, 'signal'] = 'buy'

        # Sell signal: when RSI is high (e.g., >70) or momentum turns negative.
        sell_condition = (df['rsi'] > 70) | (df['momentum'] < 0)
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

            if signal_type == 'buy' and not in_position:
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
    price_data = pd.DataFrame({
        'datetime': dates,
        'open': prices + np.random.randn(100)*0.5,
        'high': prices + np.random.rand(100),
        'low': prices - np.random.rand(100),
        'close': prices,
        'volume': np.random.randint(100, 1000, size=100)
    })

    strategy = ComboStrategyExample()
    signals = strategy.generate_signals(price_data)
    print("Generated Signals:")
    print(signals.head())
    trades = strategy.generate_trades(price_data, signals)
    print("\nSimulated Trades:")
    print(trades.head())

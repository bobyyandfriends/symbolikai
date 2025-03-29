#!/usr/bin/env python3
import pandas as pd
import numpy as np
from base_strategy import BaseStrategy

class SimpleStrategy(BaseStrategy):
    """
    A simple strategy implementation that calculates RSI and SMA to generate signals,
    and simulates trades based on these signals.
    """
    def __init__(self, rsi_period: int = 14, sma_period: int = 50,
                 rsi_buy_threshold: float = 30, rsi_sell_threshold: float = 70, **kwargs):
        super().__init__(name="SimpleStrategy", **kwargs)
        self.rsi_period = rsi_period
        self.sma_period = sma_period
        self.rsi_buy_threshold = rsi_buy_threshold
        self.rsi_sell_threshold = rsi_sell_threshold

    def apply_indicators(self, price_data: pd.DataFrame) -> pd.DataFrame:
        df = price_data.copy().sort_values('datetime').reset_index(drop=True)
        delta = df['close'].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(window=self.rsi_period, min_periods=self.rsi_period).mean()
        avg_loss = loss.rolling(window=self.rsi_period, min_periods=self.rsi_period).mean()
        rs = avg_gain / (avg_loss + 1e-10)  # Avoid division by zero
        df['rsi'] = 100 - (100 / (1 + rs))
        df['sma'] = df['close'].rolling(window=self.sma_period, min_periods=self.sma_period).mean()
        return df

    def generate_signals(self, price_data: pd.DataFrame, signal_data: pd.DataFrame = None) -> pd.DataFrame:
        df = self.apply_indicators(price_data)
        # Ensure we have enough data for indicators
        df = df.dropna(subset=['rsi', 'sma']).copy()
        df['signal'] = None

        # Generate buy signal: RSI below buy threshold and price above SMA
        buy_condition = (df['rsi'] < self.rsi_buy_threshold) & (df['close'] > df['sma'])
        df.loc[buy_condition, 'signal'] = 'buy'

        # Generate sell signal: RSI above sell threshold and price below SMA
        sell_condition = (df['rsi'] > self.rsi_sell_threshold) & (df['close'] < df['sma'])
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
            # Get the nearest price data at or after the signal time
            current_row = price_df[price_df['datetime'] >= signal_time].iloc[0]
            current_price = current_row['close']

            if signal_type == 'buy' and not in_position:
                in_position = True
                entry_time = current_row['datetime']
                entry_price = current_price
            elif signal_type == 'sell' and in_position:
                exit_time = current_row['datetime']
                exit_price = current_price
                profit = exit_price - entry_price  # For long positions
                trades.append({
                    'entry_time': entry_time,
                    'entry_price': entry_price,
                    'exit_time': exit_time,
                    'exit_price': exit_price,
                    'profit': profit
                })
                in_position = False
                entry_time, entry_price = None, None

        # Close any open position at the end of the data
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
    # Example usage with dummy data for testing
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

    strategy = SimpleStrategy()
    signals = strategy.generate_signals(price_data)
    print("Generated Signals:")
    print(signals.head())
    trades = strategy.generate_trades(price_data, signals)
    print("\nSimulated Trades:")
    print(trades.head())

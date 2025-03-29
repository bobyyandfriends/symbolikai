#!/usr/bin/env python3
import matplotlib.pyplot as plt
import pandas as pd

def plot_strategy_summary(price_data: pd.DataFrame, trades: pd.DataFrame, signals: pd.DataFrame, indicators: pd.DataFrame = None):
    """
    Plots a comprehensive strategy summary that includes:
      - Price data (close prices)
      - Trade entries (green markers) and exits (red markers) with connecting lines
      - Signal markers (blue for buy, orange for sell)
      - Optional indicator overlays (e.g., SMA, RSI) if provided in the indicators DataFrame
    
    Parameters:
      price_data: DataFrame containing at least 'datetime' and 'close' columns.
      trades: DataFrame with columns 'entry_time', 'entry_price', 'exit_time', 'exit_price'.
      signals: DataFrame with columns 'datetime' and 'signal'.
      indicators: Optional DataFrame with 'datetime' and one or more indicator columns.
    """
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # Plot the price data
    ax.plot(price_data['datetime'], price_data['close'], label="Close Price", color="black")
    
    # Plot trade entries and exits
    for idx, trade in trades.iterrows():
        ax.scatter(trade['entry_time'], trade['entry_price'], marker="^", color="green", s=100,
                   label="Trade Entry" if idx == 0 else "")
        ax.scatter(trade['exit_time'], trade['exit_price'], marker="v", color="red", s=100,
                   label="Trade Exit" if idx == 0 else "")
        ax.plot([trade['entry_time'], trade['exit_time']], [trade['entry_price'], trade['exit_price']],
                linestyle="--", color="gray", alpha=0.7)
    
    # Plot signal markers
    # For this example, we assume signal types contain the word "buy" or "sell"
    buy_signals = signals[signals['signal'].str.contains("buy", case=False)]
    sell_signals = signals[signals['signal'].str.contains("sell", case=False)]
    
    if not buy_signals.empty:
        # Use the price at the signal time (match using datetime index from price_data)
        price_index = price_data.set_index('datetime')
        ax.scatter(buy_signals['datetime'], price_index.loc[buy_signals['datetime'], 'close'],
                   marker="o", color="blue", s=80, label="Buy Signal")
    
    if not sell_signals.empty:
        price_index = price_data.set_index('datetime')
        ax.scatter(sell_signals['datetime'], price_index.loc[sell_signals['datetime'], 'close'],
                   marker="o", color="orange", s=80, label="Sell Signal")
    
    # Overlay indicator data if provided
    if indicators is not None:
        for col in indicators.columns:
            if col != "datetime":
                ax.plot(indicators["datetime"], indicators[col], label=col)
    
    ax.set_title("Strategy Summary: Price, Trades, and Signals")
    ax.set_xlabel("Datetime")
    ax.set_ylabel("Price")
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Example usage with dummy data:
    import numpy as np
    from datetime import datetime, timedelta
    
    # Create dummy price data
    dates = pd.date_range(start="2022-01-01", periods=100, freq='D')
    np.random.seed(42)
    prices = np.cumsum(np.random.randn(100)) + 100
    price_data = pd.DataFrame({
        'datetime': dates,
        'close': prices
    })
    
    # Dummy trades data
    trades = pd.DataFrame({
        'entry_time': [dates[10], dates[50]],
        'entry_price': [prices[10], prices[50]],
        'exit_time': [dates[30], dates[70]],
        'exit_price': [prices[30], prices[70]]
    })
    
    # Dummy signals data
    signals = pd.DataFrame({
        'datetime': [dates[10], dates[30], dates[50], dates[70]],
        'signal': ['buy', 'sell', 'buy', 'sell']
    })
    
    # Dummy indicators (e.g., 10-day SMA)
    sma = price_data['close'].rolling(window=10, min_periods=10).mean()
    indicators = pd.DataFrame({
        'datetime': price_data['datetime'],
        'SMA_10': sma
    }).dropna()
    
    plot_strategy_summary(price_data, trades, signals, indicators)

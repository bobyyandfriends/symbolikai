#!/usr/bin/env python3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_trades(price_data: pd.DataFrame, trades: pd.DataFrame):
    """
    Plot the price data with entry and exit markers for each trade.
    Expects price_data to have a 'datetime' and 'close' column.
    Trades DataFrame should include 'entry_time', 'entry_price', 'exit_time', 'exit_price'.
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot the price data
    ax.plot(price_data['datetime'], price_data['close'], label="Close Price", color='blue')
    
    # Plot each trade entry and exit
    for idx, trade in trades.iterrows():
        entry_time = trade['entry_time']
        entry_price = trade['entry_price']
        exit_time = trade['exit_time']
        exit_price = trade['exit_price']
        
        ax.scatter(entry_time, entry_price, marker="^", color="green", s=100, label="Entry" if idx == 0 else "")
        ax.scatter(exit_time, exit_price, marker="v", color="red", s=100, label="Exit" if idx == 0 else "")
        ax.plot([entry_time, exit_time], [entry_price, exit_price], color="gray", linestyle="--", linewidth=1)
    
    ax.set_title("Price Chart with Trades")
    ax.set_xlabel("Datetime")
    ax.set_ylabel("Price")
    ax.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_equity_curve(trades: pd.DataFrame, initial_capital: float = 100000):
    """
    Plot the equity curve based on executed trades.
    The function simulates the equity curve by summing trade profits sequentially.
    """
    equity = [initial_capital]
    for profit in trades['profit']:
        equity.append(equity[-1] + profit)
    equity = np.array(equity)
    
    # Generate a corresponding datetime series using trade exit times
    exit_times = trades['exit_time'].tolist()
    # Add a starting time (using the first trade's entry time or a dummy date if no trades)
    if not trades.empty:
        start_time = trades.iloc[0]['entry_time']
    else:
        start_time = pd.Timestamp.now()
    times = [start_time] + exit_times
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(times, equity, label="Equity Curve", color="purple")
    ax.set_title("Equity Curve")
    ax.set_xlabel("Datetime")
    ax.set_ylabel("Equity")
    ax.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_signals(price_data: pd.DataFrame, signals: pd.DataFrame):
    """
    Plot the price data and overlay generated signals.
    The signals DataFrame should include 'datetime' and 'signal' columns.
    Different markers/colors are used for buy and sell signals.
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(price_data['datetime'], price_data['close'], label="Close Price", color='blue')
    
    # Separate buy and sell signals
    buy_signals = signals[signals['signal'].str.contains('buy', case=False)]
    sell_signals = signals[signals['signal'].str.contains('sell', case=False)]
    
    ax.scatter(buy_signals['datetime'], 
               price_data.set_index('datetime').loc[buy_signals['datetime'], 'close'],
               marker="^", color="green", s=100, label="Buy Signal")
    
    ax.scatter(sell_signals['datetime'], 
               price_data.set_index('datetime').loc[sell_signals['datetime'], 'close'],
               marker="v", color="red", s=100, label="Sell Signal")
    
    ax.set_title("Price Chart with Signal Overlays")
    ax.set_xlabel("Datetime")
    ax.set_ylabel("Price")
    ax.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Example usage with dummy data:
    import pandas as pd
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

    # Create dummy signals data (simulate some buy and sell signals)
    signals = pd.DataFrame({
        'datetime': [dates[10], dates[30], dates[50], dates[70]],
        'signal': ['buy', 'sell', 'buy', 'sell']
    })

    # Create dummy trades data
    trades = pd.DataFrame({
        'entry_time': [dates[10], dates[50]],
        'entry_price': [prices[10], prices[50]],
        'exit_time': [dates[30], dates[70]],
        'exit_price': [prices[30], prices[70]],
        'profit': [prices[30] - prices[10], prices[70] - prices[50]]
    })

    # Plot each visualization
    plot_trades(price_data, trades)
    plot_equity_curve(trades, initial_capital=100000)
    plot_signals(price_data, signals)

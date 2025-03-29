#!/usr/bin/env python3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_equity_curve(trades: pd.DataFrame, initial_capital: float = 100000):
    """
    Plot the equity curve based on executed trades.
    
    Expects trades DataFrame to contain:
      - 'entry_time' (datetime of trade entry)
      - 'exit_time' (datetime of trade exit)
      - 'profit' (profit or loss from the trade)
    
    The function simulates the equity curve by starting with the initial capital
    and adding each trade's profit sequentially. The exit times are used as x-axis.
    """
    if trades.empty:
        print("No trades available to plot equity curve.")
        return

    # Ensure trades are sorted by exit time
    trades = trades.sort_values('exit_time').reset_index(drop=True)

    # Initialize equity curve list with starting capital
    equity = [initial_capital]
    times = [trades.iloc[0]['entry_time']]
    
    # Update equity based on trade profits
    for _, trade in trades.iterrows():
        equity.append(equity[-1] + trade['profit'])
        times.append(trade['exit_time'])
    
    equity_df = pd.DataFrame({
        'time': times,
        'equity': equity
    })

    # Plot the equity curve
    plt.figure(figsize=(12, 6))
    plt.plot(equity_df['time'], equity_df['equity'], marker='o', label='Equity Curve', color='purple')
    plt.xlabel("Time")
    plt.ylabel("Equity")
    plt.title("Equity Curve")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Example usage with dummy trades:
    from datetime import datetime, timedelta

    # Create sample trades data
    trades_data = [
        {
            'entry_time': datetime(2022, 1, 1),
            'exit_time': datetime(2022, 1, 5),
            'profit': 500
        },
        {
            'entry_time': datetime(2022, 1, 10),
            'exit_time': datetime(2022, 1, 15),
            'profit': -200
        },
        {
            'entry_time': datetime(2022, 1, 20),
            'exit_time': datetime(2022, 1, 25),
            'profit': 300
        }
    ]
    trades = pd.DataFrame(trades_data)
    plot_equity_curve(trades, initial_capital=100000)

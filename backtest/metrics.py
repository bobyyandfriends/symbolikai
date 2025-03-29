#!/usr/bin/env python3
import pandas as pd
import numpy as np

def calculate_metrics(trades: pd.DataFrame, initial_capital: float = 100000) -> dict:
    """
    Calculate performance metrics for a set of trades.
    
    Metrics include:
      - Total return (as percentage of initial capital)
      - Win rate (percentage of trades with positive profit)
      - Average profit per trade
      - Maximum drawdown (percentage)
      - Number of trades executed
      - Average holding period (in days)
      
    Parameters:
      trades: DataFrame containing trade logs with columns:
              'entry_time', 'exit_time', 'entry_price', 'exit_price', 'profit'
      initial_capital: starting capital amount
      
    Returns:
      A dictionary with the calculated metrics.
    """
    if trades.empty:
        return {
            'total_return_percent': 0.0,
            'win_rate_percent': 0.0,
            'avg_profit': 0.0,
            'max_drawdown_percent': 0.0,
            'num_trades': 0,
            'avg_holding_days': 0.0
        }
    
    trades = trades.copy()
    # Calculate profit as a percentage of initial capital for each trade
    trades['profit_pct'] = trades['profit'] / initial_capital
    total_return = trades['profit_pct'].sum() * 100  # percentage

    num_trades = len(trades)
    wins = trades[trades['profit'] > 0]
    win_rate = (len(wins) / num_trades) * 100  # percentage
    avg_profit = trades['profit'].mean()

    # Build an equity curve to compute max drawdown
    equity_curve = [initial_capital]
    for profit in trades['profit']:
        equity_curve.append(equity_curve[-1] + profit)
    equity_curve = np.array(equity_curve)
    running_max = np.maximum.accumulate(equity_curve)
    drawdowns = (running_max - equity_curve) / running_max
    max_drawdown = drawdowns.max() * 100  # percentage

    # Calculate average holding period in days
    if 'entry_time' in trades.columns and 'exit_time' in trades.columns:
        trades['holding_days'] = (pd.to_datetime(trades['exit_time']) - pd.to_datetime(trades['entry_time'])).dt.days
        avg_holding_days = trades['holding_days'].mean()
    else:
        avg_holding_days = None

    return {
        'total_return_percent': total_return,
        'win_rate_percent': win_rate,
        'avg_profit': avg_profit,
        'max_drawdown_percent': max_drawdown,
        'num_trades': num_trades,
        'avg_holding_days': avg_holding_days
    }

if __name__ == "__main__":
    # Example usage:
    from datetime import datetime, timedelta

    # Create sample trades data
    trades_data = [
        {
            'entry_time': datetime(2022, 1, 1),
            'entry_price': 100,
            'exit_time': datetime(2022, 1, 5),
            'exit_price': 105,
            'profit': 5
        },
        {
            'entry_time': datetime(2022, 1, 10),
            'entry_price': 106,
            'exit_time': datetime(2022, 1, 15),
            'exit_price': 104,
            'profit': -2
        },
        {
            'entry_time': datetime(2022, 1, 20),
            'entry_price': 103,
            'exit_time': datetime(2022, 1, 25),
            'exit_price': 108,
            'profit': 5
        }
    ]
    trades_df = pd.DataFrame(trades_data)
    metrics = calculate_metrics(trades_df, initial_capital=100000)
    print("Calculated Metrics:")
    print(metrics)

#!/usr/bin/env python3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from datetime import datetime

def compare_equity_curves(results_list):
    """
    Compare equity curves for multiple strategy backtests.
    Each element in results_list is expected to be a dictionary returned from run_backtest,
    containing at least:
      - 'trades': a DataFrame with trade logs including 'entry_time', 'exit_time', 'profit'
      - 'config': a dictionary with an 'initial_capital' key (default=100000 if not provided)
      - 'strategy_name': a string identifier for the strategy.
    
    This function simulates each equity curve by starting with the initial capital and
    adding each trade's profit sequentially (sorted by exit time), then plots all curves.
    """
    plt.figure(figsize=(14, 7))
    
    for result in results_list:
        strategy_name = result.get("strategy_name", "Unknown")
        trades = result.get("trades")
        config = result.get("config", {})
        initial_capital = config.get("initial_capital", 100000)
        
        # Ensure trades are sorted by exit time
        trades = trades.sort_values("exit_time").reset_index(drop=True)
        
        # Compute equity curve
        equity = [initial_capital]
        times = [trades.iloc[0]["entry_time"]] if not trades.empty else [datetime.now()]
        for _, trade in trades.iterrows():
            equity.append(equity[-1] + trade["profit"])
            times.append(trade["exit_time"])
        
        plt.plot(times, equity, marker="o", label=strategy_name)
    
    plt.xlabel("Time")
    plt.ylabel("Equity")
    plt.title("Comparison of Equity Curves Across Strategies")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def compare_metrics(results_list):
    """
    Compare performance metrics across multiple strategy backtests.
    Each element in results_list should contain:
      - 'strategy_name': identifier for the strategy
      - 'metrics': a dictionary with performance metrics (e.g., total_return_percent, win_rate_percent, etc.)
    
    This function builds a DataFrame with strategies as rows and metrics as columns,
    prints the table, and visualizes the comparison with a seaborn heatmap.
    """
    records = []
    for result in results_list:
        strategy_name = result.get("strategy_name", "Unknown")
        metrics = result.get("metrics", {})
        record = {"Strategy": strategy_name}
        record.update(metrics)
        records.append(record)
    
    metrics_df = pd.DataFrame(records)
    metrics_df.set_index("Strategy", inplace=True)
    
    print("Comparison of Metrics:")
    print(metrics_df)
    
    plt.figure(figsize=(10, 6))
    sns.heatmap(metrics_df, annot=True, fmt=".2f", cmap="YlGnBu")
    plt.title("Performance Metrics Comparison")
    plt.tight_layout()
    plt.show()
    
    return metrics_df

if __name__ == "__main__":
    # Example usage with dummy backtest results for two strategies:
    from datetime import timedelta

    # Dummy results for Strategy A
    dates_a = pd.date_range(start="2022-01-01", periods=5, freq='D')
    trades_a = pd.DataFrame({
        "entry_time": [dates_a[0], dates_a[2]],
        "entry_price": [100, 102],
        "exit_time": [dates_a[1], dates_a[4]],
        "exit_price": [105, 101],
        "profit": [5, -1]
    })
    metrics_a = {
        "total_return_percent": 4.0,
        "win_rate_percent": 50.0,
        "avg_profit": 2.0,
        "max_drawdown_percent": 3.0,
        "num_trades": 2,
        "avg_holding_days": 2.5
    }
    result_a = {
        "strategy_name": "Strategy A",
        "trades": trades_a,
        "config": {"initial_capital": 100000},
        "metrics": metrics_a,
        "datetime": datetime.now()
    }

    # Dummy results for Strategy B
    dates_b = pd.date_range(start="2022-01-01", periods=6, freq='D')
    trades_b = pd.DataFrame({
        "entry_time": [dates_b[0], dates_b[3]],
        "entry_price": [100, 103],
        "exit_time": [dates_b[2], dates_b[5]],
        "exit_price": [102, 107],
        "profit": [2, 4]
    })
    metrics_b = {
        "total_return_percent": 3.0,
        "win_rate_percent": 100.0,
        "avg_profit": 3.0,
        "max_drawdown_percent": 2.0,
        "num_trades": 2,
        "avg_holding_days": 3.0
    }
    result_b = {
        "strategy_name": "Strategy B",
        "trades": trades_b,
        "config": {"initial_capital": 100000},
        "metrics": metrics_b,
        "datetime": datetime.now()
    }

    results_list = [result_a, result_b]
    compare_equity_curves(results_list)
    compare_metrics(results_list)

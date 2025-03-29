#!/usr/bin/env python3
import pandas as pd

def generate_trade_log(trades: pd.DataFrame) -> pd.DataFrame:
    """
    Generate a detailed trade log by adding calculated fields such as holding period (in days).
    Expects the trades DataFrame to contain:
      - 'entry_time'
      - 'exit_time'
      - 'entry_price'
      - 'exit_price'
      - 'profit'
    
    Returns:
      A new DataFrame with an added 'holding_period' column.
    """
    trade_log = trades.copy()
    # Ensure that entry_time and exit_time are datetime objects
    trade_log['entry_time'] = pd.to_datetime(trade_log['entry_time'])
    trade_log['exit_time'] = pd.to_datetime(trade_log['exit_time'])
    # Calculate holding period in days
    trade_log['holding_period'] = (trade_log['exit_time'] - trade_log['entry_time']).dt.total_seconds() / (24 * 3600)
    return trade_log

def export_trades_to_csv(trades: pd.DataFrame, path: str):
    """
    Export the generated trade log to a CSV file.
    """
    trade_log = generate_trade_log(trades)
    trade_log.to_csv(path, index=False)
    print(f"Trade log exported to: {path}")

def print_performance_summary(metrics: dict):
    """
    Nicely print the performance summary based on the provided metrics dictionary.
    """
    print("Performance Summary:")
    for key, value in metrics.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")

def export_summary_to_txt(metrics: dict, path: str):
    """
    Export the performance summary to a text file.
    """
    lines = ["Performance Summary:"]
    for key, value in metrics.items():
        lines.append(f"{key.replace('_', ' ').title()}: {value}")
    summary_text = "\n".join(lines)
    with open(path, "w") as f:
        f.write(summary_text)
    print(f"Performance summary exported to: {path}")

if __name__ == "__main__":
    # Example usage:
    from datetime import datetime

    trades_data = [
        {
            'entry_time': datetime(2022, 1, 1),
            'exit_time': datetime(2022, 1, 5),
            'entry_price': 100,
            'exit_price': 105,
            'profit': 5
        },
        {
            'entry_time': datetime(2022, 1, 10),
            'exit_time': datetime(2022, 1, 15),
            'entry_price': 106,
            'exit_price': 104,
            'profit': -2
        },
        {
            'entry_time': datetime(2022, 1, 20),
            'exit_time': datetime(2022, 1, 25),
            'entry_price': 103,
            'exit_price': 108,
            'profit': 5
        }
    ]
    trades_df = pd.DataFrame(trades_data)
    trade_log = generate_trade_log(trades_df)
    print("Trade Log:")
    print(trade_log)
    
    # Example metrics dictionary
    metrics = {
        'total_return_percent': 8.0,
        'win_rate_percent': 66.67,
        'avg_profit': 2.67,
        'max_drawdown_percent': 5.0,
        'num_trades': 3,
        'avg_holding_days': trade_log['holding_period'].mean()
    }
    
    print("\n")
    print_performance_summary(metrics)
    
    # Optionally, export trades and summary to files
    export_trades_to_csv(trades_df, "trade_log.csv")
    export_summary_to_txt(metrics, "performance_summary.txt")

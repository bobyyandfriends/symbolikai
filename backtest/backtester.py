#!/usr/bin/env python3
import pandas as pd
import numpy as np
from datetime import datetime

def calculate_metrics(trades: pd.DataFrame, initial_capital: float = 100000) -> dict:
    """
    Compute performance metrics from executed trades:
      - Total return (in percentage of initial capital)
      - Win rate (proportion of winning trades)
      - Average profit per trade
      - Maximum drawdown (using the simulated equity curve)
      - Number of trades executed
    """
    if trades.empty:
        return {
            'total_return': 0.0,
            'win_rate': 0.0,
            'avg_profit': 0.0,
            'max_drawdown': 0.0,
            'num_trades': 0
        }
    
    trades = trades.copy()
    # Calculate profit percentage for each trade relative to initial capital
    trades['profit_pct'] = trades['profit'] / initial_capital
    total_return = trades['profit_pct'].sum()
    
    num_trades = len(trades)
    wins = trades[trades['profit'] > 0]
    win_rate = len(wins) / num_trades if num_trades > 0 else 0.0
    avg_profit = trades['profit'].mean() if num_trades > 0 else 0.0

    # Build equity curve for drawdown calculation
    equity_curve = [initial_capital]
    for profit in trades['profit']:
        equity_curve.append(equity_curve[-1] + profit)
    equity_curve = np.array(equity_curve)
    running_max = np.maximum.accumulate(equity_curve)
    drawdowns = (running_max - equity_curve) / running_max
    max_drawdown = drawdowns.max()

    return {
        'total_return': total_return,
        'win_rate': win_rate,
        'avg_profit': avg_profit,
        'max_drawdown': max_drawdown,
        'num_trades': num_trades
    }

def run_backtest(strategy, price_data: pd.DataFrame, signals: pd.DataFrame, config: dict) -> dict:
    """
    Run a backtest using a given strategy, price data, and signals.
    The config dictionary can include parameters like initial_capital, slippage, commission, etc.
    
    Returns a dictionary containing:
      - trades: DataFrame of executed trades
      - metrics: Performance metrics for the backtest
      - config: The configuration used
      - strategy_name: The name of the strategy
      - timestamp: Time when the backtest was run
    """
    # Generate trades using the strategy's logic
    trades = strategy.generate_trades(price_data, signals)
    
    initial_capital = config.get("initial_capital", 100000)
    # For now, slippage and commissions are not modeled; these could be added here.
    
    metrics = calculate_metrics(trades, initial_capital=initial_capital)
    
    result = {
        "trades": trades,
        "metrics": metrics,
        "config": config,
        "strategy_name": strategy.name,
        "timestamp": datetime.now()
    }
    return result

if __name__ == "__main__":
    # Example usage:
    # Create dummy historical price data
    np.random.seed(42)
    dates = pd.date_range(start="2022-01-01", periods=100, freq='D')
    prices = np.cumsum(np.random.randn(100)) + 100
    price_data = pd.DataFrame({
        'datetime': dates,
        'open': prices + np.random.randn(100) * 0.5,
        'high': prices + np.random.rand(100),
        'low': prices - np.random.rand(100),
        'close': prices,
        'volume': np.random.randint(100, 1000, size=100)
    })

    # For signals, we'll use our SimpleStrategy implementation (from strategies/simple_strategy.py)
    from strategies.simple_strategy import SimpleStrategy
    strategy = SimpleStrategy()
    signals = strategy.generate_signals(price_data)
    
    # Set configuration parameters
    config = {
        "initial_capital": 100000,
        "slippage_pct": 0.001,  # Not applied in this simple example
        "commission": 0         # Not applied in this simple example
    }
    
    # Run the backtest
    results = run_backtest(strategy, price_data, signals, config)
    print("Backtest Metrics:")
    print(results["metrics"])
    print("\nSample Trades:")
    print(results["trades"].head())

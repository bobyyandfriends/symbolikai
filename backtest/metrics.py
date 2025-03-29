# backtest/metrics.py

from typing import List
from backtest.trade import Trade
import numpy as np
import pandas as pd

def calculate_metrics(trades: List[Trade]) -> dict:
    if not trades:
        return {
            "total_return": 0,
            "win_rate": 0,
            "avg_return": 0,
            "sharpe_ratio": 0,
            "max_drawdown": 0,
            "num_trades": 0,
            "profit_factor": 0,
            "avg_holding_days": 0,
        }

    returns = np.array([t.get_return_pct() for t in trades])
    pnls = np.array([t.calculate_pnl() for t in trades])
    durations = np.array([t.get_duration() for t in trades])

    wins = returns[returns > 0]
    losses = -returns[returns < 0]  # Make losses positive for profit factor

    total_return = np.sum(returns)
    win_rate = len(wins) / len(returns)
    avg_return = np.mean(returns)
    sharpe_ratio = (np.mean(returns) / np.std(returns)) * np.sqrt(252) if np.std(returns) > 0 else 0
    max_drawdown = compute_max_drawdown(np.cumsum(returns))
    profit_factor = (np.sum(wins) / np.sum(losses)) if np.sum(losses) > 0 else np.inf
    avg_holding_days = np.mean(durations)

    return {
        "total_return": total_return,
        "win_rate": win_rate,
        "avg_return": avg_return,
        "sharpe_ratio": sharpe_ratio,
        "max_drawdown": max_drawdown,
        "num_trades": len(trades),
        "profit_factor": profit_factor,
        "avg_holding_days": avg_holding_days
    }

def compute_max_drawdown(equity_curve: np.ndarray) -> float:
    peak = np.maximum.accumulate(equity_curve)
    drawdown = equity_curve - peak
    return np.min(drawdown)

# reporting/equity_curve.py

import matplotlib.pyplot as plt
from backtest.trade import Trade
import pandas as pd

def plot_equity_curve(trades: list[Trade]):
    """
    Plots cumulative equity over time.
    """
    if not trades:
        print("No trades to plot.")
        return

    dates = [t.exit_time for t in trades]
    equity = [1.0]  # Starting equity baseline

    for t in trades:
        pnl = t.calculate_pnl()
        equity.append(equity[-1] + pnl)

    plt.figure(figsize=(12, 4))
    plt.plot(dates, equity[1:], label="Equity Curve", color="blue")
    plt.title("Equity Curve")
    plt.xlabel("Date")
    plt.ylabel("Equity")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_drawdowns(trades: list[Trade]):
    """
    Plots drawdowns from peak equity.
    """
    if not trades:
        print("No trades to plot.")
        return

    dates = [t.exit_time for t in trades]
    equity = [1.0]

    for t in trades:
        pnl = t.calculate_pnl()
        equity.append(equity[-1] + pnl)

    equity_series = pd.Series(equity[1:], index=dates)
    running_max = equity_series.cummax()
    drawdowns = equity_series - running_max

    plt.figure(figsize=(12, 4))
    plt.plot(drawdowns.index, drawdowns.values, label="Drawdown", color="red")
    plt.title("Max Drawdowns Over Time")
    plt.xlabel("Date")
    plt.ylabel("Drawdown")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

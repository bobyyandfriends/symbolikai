# backtest/plotter.py

import matplotlib.pyplot as plt
import pandas as pd
from backtest.trade import Trade

def plot_trades(price_data: pd.DataFrame, trades: list[Trade], title="Trades on Price Chart"):
    """
    Plots price chart with trade entry and exit markers.
    """
    plt.figure(figsize=(14, 6))
    plt.plot(price_data.index, price_data["close"], label="Price", linewidth=1)

    for trade in trades:
        entry_time = trade.entry_time
        exit_time = trade.exit_time
        entry_price = trade.entry_price
        exit_price = trade.exit_price
        color = "green" if trade.side == "long" else "red"

        # Entry marker
        plt.scatter(entry_time, entry_price, marker="^", color=color)
        # Exit marker
        plt.scatter(exit_time, exit_price, marker="v", color=color)

    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_equity_curve(trades: list[Trade], title="Equity Curve"):
    """
    Plots equity growth over time based on trade returns.
    """
    if not trades:
        print("No trades to plot.")
        return

    dates = [t.exit_time for t in trades]
    equity = [1.0]  # Starting equity

    for trade in trades:
        last = equity[-1]
        pnl = trade.calculate_pnl()
        equity.append(last + pnl)

    plt.figure(figsize=(12, 4))
    plt.plot(dates, equity[1:], label="Equity Curve", linewidth=2)
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Equity")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# reporting/visualizer.py

import matplotlib.pyplot as plt
import pandas as pd

def plot_strategy_summary(price_data: pd.DataFrame, trades: list, signals: pd.DataFrame = None):
    """
    Plot full strategy view with price, entries/exits, and signals.
    """
    plt.figure(figsize=(14, 6))
    plt.plot(price_data.index, price_data["close"], label="Close", linewidth=1)

    # Entry/exit markers
    for trade in trades:
        color = "green" if trade.side == "long" else "red"
        plt.scatter(trade.entry_time, trade.entry_price, marker="^", color=color)
        plt.scatter(trade.exit_time, trade.exit_price, marker="v", color=color)

    # Overlay signals (if any)
    if signals is not None:
        for col in signals.columns:
            signal_points = signals[col].dropna()
            plt.scatter(signal_points.index, price_data.loc[signal_points.index, "close"], label=col, marker="x")

    plt.title("Strategy Summary")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_overlay_with_indicators(price_data: pd.DataFrame, indicators: pd.DataFrame):
    """
    Plot price with TA indicators (e.g., RSI, Bollinger Bands).
    """
    df = price_data.join(indicators)

    plt.figure(figsize=(14, 6))
    plt.plot(df.index, df["close"], label="Close", linewidth=1)
    
    if "rsi" in df.columns:
        plt.plot(df.index, df["rsi"], label="RSI", linestyle="--")
    if "upper_bb" in df.columns and "lower_bb" in df.columns:
        plt.plot(df.index, df["upper_bb"], label="Upper BB", linestyle=":")
        plt.plot(df.index, df["lower_bb"], label="Lower BB", linestyle=":")

    plt.title("Price + Indicators")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

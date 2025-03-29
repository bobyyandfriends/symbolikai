# reporting/signal_heatmap.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_signal_distribution(signals: pd.DataFrame):
    """
    Visualizes how signals occur by day of week and hour.
    Expects a 'signal' column and a datetime index.
    """
    if "signal" not in signals.columns:
        print("Signal column missing.")
        return

    df = signals.copy()
    df["day_of_week"] = df.index.day_name()
    df["hour"] = df.index.hour

    heatmap_data = (
        df.groupby(["day_of_week", "hour"])["signal"]
        .count()
        .unstack()
        .fillna(0)
        .reindex(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    )

    plt.figure(figsize=(12, 6))
    sns.heatmap(heatmap_data, cmap="Blues", annot=True, fmt=".0f")
    plt.title("Signal Frequency by Day & Hour")
    plt.xlabel("Hour of Day")
    plt.ylabel("Day of Week")
    plt.tight_layout()
    plt.show()


def plot_indicator_interaction_matrix(df: pd.DataFrame, indicators: list[str]):
    """
    Plots a correlation matrix of TA indicators and signals.
    Useful for checking signal redundancy or synergy.
    """
    subset = df[indicators].dropna()
    corr = subset.corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap="coolwarm", center=0)
    plt.title("Indicator Correlation Matrix")
    plt.tight_layout()
    plt.show()

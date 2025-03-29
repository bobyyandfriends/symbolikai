# backtest/backtester.py

from backtest.trade import Trade
from backtest.metrics import calculate_metrics
import pandas as pd

def run_backtest(strategy, price_data: pd.DataFrame, signal_data: pd.DataFrame, config: dict = {}) -> dict:
    """
    Run backtest using a given strategy and return trades + metrics.
    """
    df = price_data.copy()

    # Merge in signal data (assumes datetime index)
    if signal_data is not None:
        df = df.merge(signal_data, left_index=True, right_index=True, how="left")

    df = strategy.apply_indicators(df)
    df = strategy.generate_signals(df)

    trades_df = strategy.generate_trades(df)
    trade_objs = [Trade.from_row(row) for _, row in trades_df.iterrows()]

    metrics = calculate_metrics(trade_objs)

    return {
        "strategy": strategy.get_name(),
        "trades": trade_objs,
        "metrics": metrics,
        "raw": df,  # useful for charting later
    }

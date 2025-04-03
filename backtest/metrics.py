#!/usr/bin/env python3
"""
metrics.py

Contains functions to calculate key performance metrics for a set of executed trades,
including risk-adjusted metrics, synergy correlations, and optional advanced stats.
"""

import pandas as pd
import numpy as np
import math

def calculate_metrics(
    trades: pd.DataFrame, 
    initial_capital: float = 100_000.0,
    trading_days_per_year: int = 252,
    risk_free_rate: float = 0.0
) -> dict:
    """
    Calculate performance metrics from a set of trades.
    
    TRADES DataFrame expected columns:
        - entry_time   (datetime)
        - exit_time    (datetime)
        - entry_price  (float)
        - exit_price   (float)
        - profit       (float) net PnL of the trade (in currency)
        - side         (str) 'long' or 'short'
        - synergy_score (optional) float synergy or confidence measure
        - quantity     (optional) how many shares/contracts
        - commentary   (optional) text
        - reason_codes (optional) e.g. pivot/demark

    Additional parameters:
    - initial_capital: starting capital
    - trading_days_per_year: used for annualizing returns or Sharpe
    - risk_free_rate: for Sharpe or other risk metrics

    Returns a dict of various metrics:
        total_return: Sum of trade profits / initial_capital
        win_rate: fraction of positive-profit trades
        avg_profit: average profit per trade
        max_drawdown: maximum drawdown from an equity perspective
        sharpe_ratio: risk-adjusted return measure
        sortino_ratio: uses only downside volatility
        synergy_correlation: correlation between synergy_score and trade profits (if synergy_score col present)
        synergy_mean: average synergy across all trades
        exposure (optionally): time in market if you track intervals

    Customize or remove metrics as needed.
    """
    if trades.empty:
        return {
            'total_return': 0.0,
            'win_rate': 0.0,
            'avg_profit': 0.0,
            'max_drawdown': 0.0,
            'num_trades': 0,
            'sharpe_ratio': 0.0,
            'sortino_ratio': 0.0,
            'synergy_correlation': 0.0,
            'synergy_mean': 0.0
        }

    df = trades.copy()
    num_trades = len(df)
    total_profit = df['profit'].sum()
    total_return = total_profit / initial_capital
    avg_profit = df['profit'].mean()
    wins = df[df['profit'] > 0]
    win_rate = len(wins) / num_trades

    # Build equity curve to get drawdown
    equity = [initial_capital]
    for p in df['profit']:
        equity.append(equity[-1] + p)
    equity_arr = np.array(equity)
    running_max = np.maximum.accumulate(equity_arr)
    drawdowns = (running_max - equity_arr) / running_max
    max_drawdown = drawdowns.max()

    # Risk Adjusted: We'll simulate a "daily" return approach for Sharpe,
    # but we only have trade-level data, so let's approximate
    # We can transform each trade into an approximate daily return if you have
    # entry_time/exit_time. Otherwise, skip or do a simpler approach.

    # We'll do a naive approach: each trade's "return fraction" = profit / initial_capital,
    # then assume daily returns = trade_return / trade_duration in days
    # We'll store them in a list for Sharpe. This is an approximation:
    daily_returns = []
    if 'entry_time' in df.columns and 'exit_time' in df.columns:
        for _, row in df.iterrows():
            entry_t = row['entry_time']
            exit_t = row['exit_time']
            if isinstance(entry_t, pd.Timestamp) and isinstance(exit_t, pd.Timestamp):
                days_held = (exit_t - entry_t).days
                if days_held < 1:
                    days_held = 1  # to avoid zero or negative durations
                trade_return = row['profit'] / initial_capital
                daily_ret_est = trade_return / days_held
                # We put that daily_ret_est for each day to approximate
                # Actually, you'd replicate daily_ret_est * days_held times or store it once
                # We'll store once per trade for simplicity
                daily_returns.append(daily_ret_est)
            else:
                # fallback: no date info
                pass
    # if we don't have times, we skip the daily approach
    # if daily_returns empty, Sharpe will be 0

    if len(daily_returns) > 1:
        mean_daily = np.mean(daily_returns)
        std_daily = np.std(daily_returns, ddof=1)
        # annualize them
        mean_annual = mean_daily * trading_days_per_year
        std_annual = std_daily * np.sqrt(trading_days_per_year)
        if std_annual != 0:
            sharpe_ratio = (mean_annual - risk_free_rate) / std_annual
        else:
            sharpe_ratio = 0.0

        # Sortino ratio uses only negative (downside) std
        # Let's get only negative daily returns
        negative_daily = [r for r in daily_returns if r < 0]
        if len(negative_daily) > 0:
            downside_std = np.std(negative_daily, ddof=1) * np.sqrt(trading_days_per_year)
            if downside_std != 0:
                sortino_ratio = (mean_annual - risk_free_rate) / downside_std
            else:
                sortino_ratio = 0.0
        else:
            sortino_ratio = 999.0  # if no negative returns, you might define a large ratio
    else:
        sharpe_ratio = 0.0
        sortino_ratio = 0.0

    # synergy correlation
    synergy_correlation = 0.0
    synergy_mean = 0.0
    if 'synergy_score' in df.columns:
        synergy_mean = df['synergy_score'].mean()
        # correlation with profit
        if df['synergy_score'].std() > 0 and df['profit'].std() > 0:
            synergy_correlation = df['synergy_score'].corr(df['profit'])
        else:
            synergy_correlation = 0.0

    metrics = {
        'total_return': total_return,
        'win_rate': win_rate,
        'avg_profit': avg_profit,
        'max_drawdown': max_drawdown,
        'num_trades': num_trades,
        'sharpe_ratio': sharpe_ratio,
        'sortino_ratio': sortino_ratio,
        'synergy_correlation': synergy_correlation,
        'synergy_mean': synergy_mean
    }
    return metrics


def advanced_equity_stats(equity_curve: pd.DataFrame, risk_free_rate: float = 0.0) -> dict:
    """
    Optional function if you maintain a time-series equity_curve to compute 
    advanced time-series-based metrics.

    equity_curve expected columns: ['time', 'equity']
    If time is daily, we can compute daily returns. If 'time' is intraday, adjust accordingly.

    Returns stats dict e.g. for further reporting.
    """
    if equity_curve.empty or len(equity_curve) < 2:
        return {'equity_count': 0}

    df = equity_curve.copy()
    df = df.sort_values('time')  # ensure chronological
    df['pct_change'] = df['equity'].pct_change().fillna(0.0)

    # basic stats
    total_return = (df['equity'].iloc[-1] - df['equity'].iloc[0]) / df['equity'].iloc[0]
    dd_series = (df['equity'].cummax() - df['equity']) / df['equity'].cummax()
    max_dd = dd_series.max()

    # Sharpe from daily returns:
    mean_ret = df['pct_change'].mean()
    std_ret = df['pct_change'].std(ddof=1)
    sharpe = 0.0
    if std_ret != 0:
        sharpe = (mean_ret - risk_free_rate) / std_ret

    # Possibly more advanced
    negative_rets = df.loc[df['pct_change'] < 0, 'pct_change']
    if not negative_rets.empty:
        std_down = negative_rets.std(ddof=1)
        sortino = (mean_ret - risk_free_rate) / std_down if std_down != 0 else 999.0
    else:
        sortino = 999.0

    return {
        'equity_count': len(df),
        'total_return_ts': total_return,
        'max_drawdown_ts': max_dd,
        'sharpe_ts': sharpe,
        'sortino_ts': sortino
    }


if __name__ == "__main__":
    # Example usage:
    # We'll create a small trades DF for demonstration
    trades_data = [
        {
            'entry_time': pd.Timestamp("2023-01-01"),
            'exit_time': pd.Timestamp("2023-01-05"),
            'profit': 500,
            'side': 'long',
            'synergy_score': 2.2
        },
        {
            'entry_time': pd.Timestamp("2023-01-02"),
            'exit_time': pd.Timestamp("2023-01-06"),
            'profit': -200,
            'side': 'short',
            'synergy_score': 1.5
        },
        {
            'entry_time': pd.Timestamp("2023-01-03"),
            'exit_time': pd.Timestamp("2023-01-07"),
            'profit': 300,
            'side': 'long',
            'synergy_score': 3.1
        },
    ]
    trades_df = pd.DataFrame(trades_data)
    results = calculate_metrics(trades_df, initial_capital=100_000, trading_days_per_year=252)
    print("Trade Metrics:")
    for k, v in results.items():
        print(f"{k}: {v:.4f}")

    # Example equity curve data
    eq_data = [
        {'time': pd.Timestamp("2023-01-01"), 'equity': 100000},
        {'time': pd.Timestamp("2023-01-02"), 'equity': 100300},
        {'time': pd.Timestamp("2023-01-03"), 'equity': 100800},
        {'time': pd.Timestamp("2023-01-04"), 'equity': 100600},
        {'time': pd.Timestamp("2023-01-05"), 'equity': 101100},
        {'time': pd.Timestamp("2023-01-06"), 'equity': 100900},
        {'time': pd.Timestamp("2023-01-07"), 'equity': 101300},
    ]
    eq_df = pd.DataFrame(eq_data)
    eq_stats = advanced_equity_stats(eq_df)
    print("\nEquity Curve Time-Series Metrics:")
    for k, v in eq_stats.items():
        if isinstance(v, float):
            print(f"{k}: {v:.4f}")
        else:
            print(f"{k}: {v}")

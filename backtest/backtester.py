#!/usr/bin/env python3
"""
backtester.py

Extended backtest module for SymbolikAI, with optional synergy scoring,
partial Kelly sizing, memory logging, and commentary hooks.

HOW TO USE:
    1) The 'run_backtest' function is the primary entry point.
    2) Supply:
       - strategy      : A strategy object implementing generate_trades()
       - price_data    : DataFrame with OHLCV and 'datetime'
       - signals       : DataFrame with signal info (could be DeMark, pivot, synergy flags)
       - config        : Dict with additional params (capital, synergy, use_kelly, etc.)
    3) The function returns a results dict containing trades, metrics, synergy logs, etc.
"""

import pandas as pd
import numpy as np
from datetime import datetime

def calculate_metrics(trades: pd.DataFrame,
                      initial_capital: float = 100_000.0) -> dict:
    """
    Compute performance metrics from executed trades.

    trades DataFrame expected columns:
        - entry_time  (datetime)
        - entry_price (float)
        - exit_time   (datetime)
        - exit_price  (float)
        - side        (str: 'long' or 'short')
        - quantity    (float)
        - profit      (float) -> net PnL of the trade
        - synergy_score (optional float) synergy or alignment measure
        - reason_codes (optional) reason commentary or codes
    """
    if trades.empty:
        return {
            'total_return': 0.0,
            'win_rate': 0.0,
            'avg_profit': 0.0,
            'max_drawdown': 0.0,
            'num_trades': 0,
            'avg_synergy': 0.0
        }

    df = trades.copy()
    # total pnl
    total_pnl = df['profit'].sum()
    num_trades = len(df)

    # measure total return as (sum of profits / initial capital)
    total_return = total_pnl / initial_capital

    # basic win rate
    wins = df[df['profit'] > 0]
    win_rate = len(wins) / num_trades if num_trades > 0 else 0.0

    avg_profit = df['profit'].mean() if num_trades else 0.0

    # build equity curve for drawdown
    equity = [initial_capital]
    for p in df['profit']:
        equity.append(equity[-1] + p)
    equity_curve = np.array(equity)
    running_max = np.maximum.accumulate(equity_curve)
    drawdowns = (running_max - equity_curve) / running_max
    max_drawdown = drawdowns.max()

    # example synergy metric
    if 'synergy_score' in df.columns:
        avg_synergy = df['synergy_score'].mean()
    else:
        avg_synergy = 0.0

    return {
        'total_return': total_return,
        'win_rate': win_rate,
        'avg_profit': avg_profit,
        'max_drawdown': max_drawdown,
        'num_trades': num_trades,
        'avg_synergy': avg_synergy
    }


def partial_kelly(prob: float,
                  win_mult: float = 1.0,
                  lose_mult: float = 1.0,
                  fraction: float = 0.5) -> float:
    """
    Calculate partial Kelly fraction of capital given a success probability
    and approximate payoff ratio.

    :param prob: Probability of winning the trade (0 < prob < 1).
    :param win_mult: How many dollars you win for each $1 bet if you win.
    :param lose_mult: How many dollars you lose for each $1 bet if you lose (often 1.0).
    :param fraction: A scaling factor to reduce Kelly volatility (default=0.5).
    :return: fraction_of_capital_to_use
    """
    # Basic single-win Kelly formula: f* = (p * b - q) / b
    # b = win_mult / lose_mult
    # q = 1 - p
    b = win_mult / lose_mult if lose_mult != 0 else win_mult
    q = 1.0 - prob

    # raw kelly fraction
    kelly_raw = (b * prob - q) / b if b != 0 else 0.0
    # partial scale
    kelly_used = kelly_raw * fraction

    # safety clamp, 0 <= f <= 1
    kelly_used = max(0.0, min(1.0, kelly_used))
    return kelly_used


def synergy_score_calc(row: pd.Series) -> float:
    """
    Example synergy scoring function that combines multiple signals or
    alignment factors. Adjust as needed to reflect actual synergy logic.

    :param row: row of signals or features
    :return: synergy score
    """
    # placeholder: we sum up all '1' signals in the row
    # or any advanced synergy logic. e.g. row['demark'] + row['pivot'] ...
    synergy = 0.0
    # Example approach:
    if 'demark_signal' in row and row['demark_signal'] == 1:
        synergy += 1.0
    if 'pivot_signal' in row and row['pivot_signal'] == 1:
        synergy += 1.0
    if 'valuation_signal' in row and row['valuation_signal'] == 1:
        synergy += 1.0
    # etc...
    return synergy


def run_backtest(strategy,
                 price_data: pd.DataFrame,
                 signals: pd.DataFrame,
                 config: dict) -> dict:
    """
    Run a backtest using a given strategy, price data, and signals with synergy,
    partial Kelly, commentary, etc.

    :param strategy: Strategy object that must implement 'generate_trades(price_data, signals)'
    :param price_data: DataFrame of OHLCV with 'datetime'
    :param signals: DataFrame of any signals or synergy hints
    :param config: dict containing:
        - initial_capital (float)
        - use_kelly (bool)
        - kelly_fraction (float)
        - synergy_enabled (bool)
        - commentary (bool)
        - etc...
    :return: dictionary with 'trades', 'metrics', 'config', 'timestamp', ...
    """
    # 1) Generate raw trades from the strategy
    raw_trades = strategy.generate_trades(price_data, signals)

    if raw_trades.empty:
        return {
            "trades": pd.DataFrame(),
            "metrics": {},
            "config": config,
            "strategy_name": getattr(strategy, 'name', 'Unknown'),
            "timestamp": datetime.now()
        }

    # Ensure we have columns for synergy + commentary
    if 'synergy_score' not in raw_trades.columns:
        raw_trades['synergy_score'] = 0.0
    if 'commentary' not in raw_trades.columns:
        raw_trades['commentary'] = ""

    initial_capital = config.get("initial_capital", 100_000.0)
    use_kelly = config.get("use_kelly", False)
    kelly_fraction = config.get("kelly_fraction", 0.5)
    synergy_enabled = config.get("synergy_enabled", False)
    commentary_flag = config.get("commentary", False)

    # 2) Optionally compute synergy for each trade
    if synergy_enabled and not raw_trades.empty:
        # If your synergy logic is in the backtest, do it here or 
        # do synergy inside the strategy. Example:
        synergy_values = []
        for _, trow in raw_trades.iterrows():
            synergy_val = synergy_score_calc(trow)  # example
            synergy_values.append(synergy_val)
        raw_trades['synergy_score'] = synergy_values

    # 3) Apply partial Kelly if needed
    # We'll do a simple approach: For each trade, we assign a quantity
    # based on partial kelly using a dummy success probability from synergy.
    # Or maybe we have a 'probability' column from the strategy. We'll do synergy as proxy:
    if use_kelly:
        capital_available = initial_capital
        updated_qty = []
        updated_profit = []
        for idx, row in raw_trades.iterrows():
            # dummy probability from synergy_score
            # e.g. synergy_score in [0..3], map to prob = synergy_score/5 + 0.4
            synergy = row['synergy_score']
            prob_est = min(0.95, max(0.05, synergy/5 + 0.4))  # toy function
            f_cap = partial_kelly(prob_est, win_mult=1.0, lose_mult=1.0, fraction=kelly_fraction)

            # if side is 'long', we buy f_cap * capital_available / entry_price
            # here we just store it, but you'd do a more robust approach
            entry_price = row['entry_price']
            if entry_price <= 0:
                qty = 0.0
            else:
                qty = (capital_available * f_cap) / entry_price

            # approximate PnL:
            # This is naive - real approach needs to track capital changes over time
            # but let's store something
            exit_price = row['exit_price']
            side = row['side'].lower()
            if side == 'long':
                trade_pnl = (exit_price - entry_price) * qty
            else:  # short
                trade_pnl = (entry_price - exit_price) * qty

            updated_qty.append(qty)
            updated_profit.append(trade_pnl)

        raw_trades['quantity'] = updated_qty
        raw_trades['profit'] = updated_profit
    else:
        # if you don't do Kelly, we assume profit is precomputed by the strategy or set quantity = 1
        if 'quantity' not in raw_trades.columns:
            raw_trades['quantity'] = 1.0
        if 'profit' not in raw_trades.columns:
            # naive approach
            raw_trades['profit'] = raw_trades.apply(
                lambda r: (r['exit_price'] - r['entry_price']) if r['side'] == 'long'
                else (r['entry_price'] - r['exit_price']),
                axis=1
            )

    # 4) Generate commentary if requested
    # e.g., "Trade triggered by synergy=2.0, partialKelly=0.15, reason=Pivot+DeMark"
    if commentary_flag:
        new_comments = []
        for idx, row in raw_trades.iterrows():
            side = row['side']
            synergy = row['synergy_score']
            qty = row.get('quantity', 1.0)
            reason = f"Side={side}, synergy={synergy:.2f}, qty={qty:.1f}"
            row_comment = "Trade triggered. " + reason
            new_comments.append(row_comment)
        raw_trades['commentary'] = new_comments

    # 5) Calculate final metrics
    stats = calculate_metrics(raw_trades, initial_capital=initial_capital)

    # Return result structure
    result = {
        "trades": raw_trades,
        "metrics": stats,
        "config": config,
        "strategy_name": getattr(strategy, 'name', 'Unknown'),
        "timestamp": datetime.now()
    }
    return result

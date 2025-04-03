#!/usr/bin/env python3
"""
logic_checker.py

Provides a framework to compare "expected" signals against the actual trades 
executed by the strategy, optionally factoring in synergy or other fields. 

Enhancements over the original include:
1. User-defined time tolerance (± days, hours, or minutes).
2. Optional synergy checking (e.g., synergy >= threshold).
3. More robust summary stats, including matched counts, mismatch rate, 
   and potential confusion matrix if extended for multiple signal types.
4. Common use cases:
    - RSI-based "expected buy" whenever RSI < X
    - Or any rule-based approach to define expected signals.
5. A flexible approach to unify all results in a final DataFrame 
   with info on matched trades, synergy, times, etc.
"""

import pandas as pd
import numpy as np
from datetime import timedelta

def load_expected_signals(price_data: pd.DataFrame,
                          rule_func=None,
                          rsi_threshold: float = 30) -> pd.DataFrame:
    """
    Generate expected signals from price data. By default, it uses RSI < rsi_threshold => 'buy'.
    Alternatively, the user can supply a 'rule_func' that returns a string signal or 'none'.

    :param price_data: DataFrame with columns: 'datetime', 'rsi', etc.
    :param rule_func: optional user function that takes (row) -> string signal
    :param rsi_threshold: fallback threshold if no rule_func is provided
    :return: DataFrame of expected signals, columns: ['datetime','expected_signal']
    """
    df = price_data.copy().sort_values('datetime').reset_index(drop=True)
    if rule_func is not None:
        df['expected_signal'] = df.apply(lambda row: rule_func(row), axis=1)
    else:
        # fallback: RSI-based approach
        if 'rsi' not in df.columns:
            raise ValueError("price_data missing 'rsi' column for default RSI-based logic.")
        df['expected_signal'] = df['rsi'].apply(lambda x: 'buy' if x < rsi_threshold else 'none')

    # Keep only rows with actual signals (non-'none')
    expected_signals = df[df['expected_signal'] != 'none'][['datetime', 'expected_signal']]
    return expected_signals


def check_trade_logic(price_data: pd.DataFrame,
                      trades: pd.DataFrame,
                      rule_func=None,
                      rsi_threshold: float = 30,
                      time_tolerance: pd.Timedelta = timedelta(days=1),
                      synergy_check: bool = False,
                      synergy_col: str = "synergy_score",
                      synergy_thresh: float = 1.0) -> pd.DataFrame:
    """
    Compare actual trades to "expected" signals. For each expected signal row:
      - We see if there is a matching trade entry within ± time_tolerance
      - If synergy_check is True, we also verify synergy >= synergy_thresh in that trade

    Returns: DataFrame of expected signals with columns:
       'datetime', 'expected_signal', 'matched' (bool), 'trade_entry_time', 'trade_synergy', etc.
    Also prints a summary of total signals, matched signals, mismatch %, synergy stats (if used).

    :param price_data: DataFrame that can feed load_expected_signals (with 'datetime', 'rsi', etc.)
    :param trades: DataFrame of actual trades with 'entry_time' column and optionally synergy column
    :param rule_func: optional function for generating signals from price_data
    :param rsi_threshold: float for default RSI-based approach if rule_func is None
    :param time_tolerance: how close in time an actual trade must be to match an expected signal
    :param synergy_check: if True, we also confirm synergy >= synergy_thresh
    :param synergy_col: name of synergy column in trades
    :param synergy_thresh: synergy must be >= this to consider it matched
    :return: expected_signals DataFrame with match info
    """
    # 1) get the expected signals
    expected_signals = load_expected_signals(price_data, rule_func=rule_func, rsi_threshold=rsi_threshold)
    if expected_signals.empty:
        print("No expected signals found. Check your RSI threshold or rule_func.")
        return expected_signals

    # 2) add columns to track matches
    expected_signals['matched'] = False
    expected_signals['trade_entry_time'] = pd.NaT
    if synergy_check:
        expected_signals['matched_synergy'] = False
        expected_signals['trade_synergy'] = np.nan

    # ensure trades has a datetime-like 'entry_time'
    if 'entry_time' not in trades.columns:
        raise ValueError("'trades' DataFrame missing 'entry_time' column")
    trades_df = trades.copy()
    trades_df['entry_time'] = pd.to_datetime(trades_df['entry_time'])

    # 3) For each expected signal, find a trade within ± time_tolerance
    for idx, exp in expected_signals.iterrows():
        exp_time = exp['datetime']
        lower_bound = exp_time - time_tolerance
        upper_bound = exp_time + time_tolerance
        matched_trades = trades_df[
            (trades_df['entry_time'] >= lower_bound) &
            (trades_df['entry_time'] <= upper_bound)
        ]
        if not matched_trades.empty:
            # We consider the first matched trade as fulfilling the logic
            matched_trade = matched_trades.iloc[0]
            expected_signals.at[idx, 'matched'] = True
            expected_signals.at[idx, 'trade_entry_time'] = matched_trade['entry_time']

            if synergy_check and synergy_col in matched_trade:
                trade_syn = matched_trade[synergy_col]
                expected_signals.at[idx, 'trade_synergy'] = trade_syn
                # synergy match
                synergy_ok = (trade_syn >= synergy_thresh)
                expected_signals.at[idx, 'matched_synergy'] = synergy_ok

    # summary
    total_signals = len(expected_signals)
    matched = expected_signals['matched'].sum()
    mismatch_rate = 0.0
    if total_signals > 0:
        mismatch_rate = (total_signals - matched) / total_signals * 100.0

    print("Logic Checker Summary:")
    print(f"  Total Expected Signals: {total_signals}")
    print(f"  Matched Signals:       {matched}")
    print(f"  Mismatch Rate:         {mismatch_rate:.2f}%")

    if synergy_check:
        # synergy matched means 'matched == True AND matched_synergy == True'
        synergy_matches = expected_signals[(expected_signals['matched'] == True) &
                                           (expected_signals['matched_synergy'] == True)]
        synergy_count = len(synergy_matches)
        print(f"  Synergy-based matches: {synergy_count}")

    return expected_signals


if __name__ == "__main__":
    import numpy as np
    from datetime import datetime, timedelta

    # Create dummy price data with an RSI column
    dates = pd.date_range(start="2022-01-01", periods=30, freq='D')
    np.random.seed(42)
    prices = np.cumsum(np.random.randn(30)) + 100
    price_data = pd.DataFrame({
        'datetime': dates,
        'close': prices
    })
    # Dummy RSI: sinusoidal pattern
    price_data['rsi'] = 50 + 10 * np.sin(np.linspace(0, 6, 30))

    # Make some trades
    trades_data = [
        {
            'entry_time': dates[5], 
            'entry_price': 101.5, 
            'exit_time': dates[8],
            'exit_price': 103.2,
            'synergy_score': 1.8
        },
        {
            'entry_time': dates[15],
            'entry_price': 105.0,
            'exit_time': dates[20],
            'exit_price': 106.0,
            'synergy_score': 2.2
        }
    ]
    trades = pd.DataFrame(trades_data)

    # Example usage: We want "buy" if RSI < 45
    # We'll use synergy_check with synergy_thresh=2.0 to see if synergy is also >=2
    checker_df = check_trade_logic(
        price_data=price_data,
        trades=trades,
        rsi_threshold=45,
        time_tolerance=timedelta(days=2),
        synergy_check=True,
        synergy_col='synergy_score',
        synergy_thresh=2.0
    )

    print("\nExpected signals with match info:")
    print(checker_df)

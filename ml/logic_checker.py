#!/usr/bin/env python3
import pandas as pd

def load_expected_signals(price_data: pd.DataFrame, threshold: float = 30) -> pd.DataFrame:
    """
    Generate expected buy signals from price data.
    For demonstration, we assume that when RSI is below the threshold,
    an expected 'buy' signal should occur.
    
    Expects price_data to have:
      - 'datetime'
      - 'rsi'
    
    Returns a DataFrame with 'datetime' and 'expected_signal' columns.
    """
    df = price_data.copy().sort_values('datetime').reset_index(drop=True)
    df['expected_signal'] = df['rsi'].apply(lambda x: 'buy' if x < threshold else 'none')
    expected_signals = df[df['expected_signal'] == 'buy'][['datetime', 'expected_signal']]
    return expected_signals

def check_trade_logic(price_data: pd.DataFrame, signals: pd.DataFrame, trades: pd.DataFrame, threshold: float = 30) -> pd.DataFrame:
    """
    Compare the actual trades against expected signals computed from the price_data.
    
    For each expected buy signal (RSI below threshold), check if a trade was opened within ±1 day.
    Returns a DataFrame of expected signals augmented with:
      - a 'matched' flag indicating whether an actual trade was found near that time,
      - and the matched trade's entry time (if any).
      
    Also prints a summary of total expected signals, matched signals, and mismatch rate.
    """
    expected_signals = load_expected_signals(price_data, threshold)
    expected_signals['matched'] = False
    expected_signals['trade_entry_time'] = pd.NaT
    
    # For each expected signal, search for a trade entry within ±1 day
    for idx, exp in expected_signals.iterrows():
        exp_time = exp['datetime']
        matched_trades = trades[
            (pd.to_datetime(trades['entry_time']) >= exp_time - pd.Timedelta(days=1)) &
            (pd.to_datetime(trades['entry_time']) <= exp_time + pd.Timedelta(days=1))
        ]
        if not matched_trades.empty:
            expected_signals.at[idx, 'matched'] = True
            expected_signals.at[idx, 'trade_entry_time'] = matched_trades.iloc[0]['entry_time']
    
    total_expected = len(expected_signals)
    matched = expected_signals['matched'].sum()
    mismatch_rate = ((total_expected - matched) / total_expected * 100) if total_expected > 0 else 0.0
    
    print("Logic Checker Summary:")
    print(f"  Total Expected Signals: {total_expected}")
    print(f"  Matched Signals: {matched}")
    print(f"  Mismatch Rate: {mismatch_rate:.2f}%")
    
    return expected_signals

if __name__ == "__main__":
    # Example usage:
    import numpy as np
    from datetime import datetime, timedelta
    
    # Create dummy price data with an RSI column
    dates = pd.date_range(start="2022-01-01", periods=100, freq='D')
    np.random.seed(42)
    prices = np.cumsum(np.random.randn(100)) + 100
    price_data = pd.DataFrame({
        'datetime': dates,
        'close': prices
    })
    # Dummy RSI values: simulate a sinusoidal pattern for demonstration
    price_data['rsi'] = 50 + 10 * np.sin(np.linspace(0, 10, 100))
    
    # Generate expected signals using a threshold (e.g., 45 for demonstration)
    signals = load_expected_signals(price_data, threshold=45)
    
    # Create dummy trades: simulate trades executed on some days
    trades_data = []
    for d in dates[::10]:
        trades_data.append({
            'entry_time': d,
            'entry_price': price_data[price_data['datetime'] == d]['close'].values[0],
            'exit_time': d + timedelta(days=2),
            'exit_price': price_data[price_data['datetime'] == d]['close'].values[0] + np.random.randn() * 2,
            'profit': np.random.randn() * 5
        })
    trades = pd.DataFrame(trades_data)
    
    # Run the logic checker
    expected_signals_checked = check_trade_logic(price_data, signals, trades, threshold=45)
    print("\nExpected Signals with Match Info:")
    print(expected_signals_checked.head())

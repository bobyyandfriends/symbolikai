#!/usr/bin/env python3
import pandas as pd
import streamlit as st

def display_trade_log(trades: pd.DataFrame) -> pd.DataFrame:
    """
    Display a styled trade log table.
    
    Highlights profitable trades in green and losing trades in red.
    Expects the trades DataFrame to have a 'profit' column.
    """
    if trades.empty:
        st.write("No trades to display.")
        return trades

    def color_profit(val):
        color = 'lightgreen' if val > 0 else 'salmon'
        return f'background-color: {color}'

    styled = trades.style.applymap(color_profit, subset=['profit'])
    st.dataframe(styled)
    return styled

def display_metrics_table(metrics: dict) -> pd.DataFrame:
    """
    Convert a metrics dictionary into a DataFrame and display it.
    """
    metrics_df = pd.DataFrame([metrics])
    st.table(metrics_df)
    return metrics_df

if __name__ == "__main__":
    # Example usage with dummy data:
    dummy_trades = pd.DataFrame({
        'entry_time': ['2022-01-01', '2022-01-10', '2022-01-20'],
        'exit_time': ['2022-01-05', '2022-01-15', '2022-01-25'],
        'entry_price': [100, 102, 101],
        'exit_price': [105, 101, 108],
        'profit': [5, -1, 7]
    })
    
    dummy_metrics = {
        'total_return_percent': 4.0,
        'win_rate_percent': 66.67,
        'avg_profit': 3.67,
        'max_drawdown_percent': 2.5,
        'num_trades': 3,
        'avg_holding_days': 4.0
    }
    
    print("Trade Log Table:")
    display_trade_log(dummy_trades)
    print("Metrics Table:")
    display_metrics_table(dummy_metrics)

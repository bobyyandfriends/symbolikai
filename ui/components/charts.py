#!/usr/bin/env python3
import pandas as pd
import plotly.graph_objects as go

def create_price_chart(price_data: pd.DataFrame, signals: pd.DataFrame = None, trades: pd.DataFrame = None) -> go.Figure:
    """
    Create an interactive price chart with optional overlays for signals and trades.
    
    Parameters:
      price_data: DataFrame containing at least 'datetime' and 'close' columns.
      signals: Optional DataFrame with columns 'datetime' and 'signal' (e.g., 'buy' or 'sell').
      trades: Optional DataFrame with columns 'entry_time', 'entry_price', 'exit_time', 'exit_price'.
      
    Returns:
      A Plotly Figure object.
    """
    fig = go.Figure()
    
    # Plot the price line
    fig.add_trace(go.Scatter(
        x=price_data['datetime'],
        y=price_data['close'],
        mode='lines',
        name='Close Price'
    ))
    
    # Overlay signals if provided
    if signals is not None and not signals.empty:
        # Separate buy and sell signals
        buy_signals = signals[signals['signal'].str.contains("buy", case=False, na=False)]
        sell_signals = signals[signals['signal'].str.contains("sell", case=False, na=False)]
        
        if not buy_signals.empty:
            # Align buy signal prices with the price data using asof merge logic
            price_index = price_data.set_index('datetime')
            buy_prices = price_index.loc[buy_signals['datetime'], 'close']
            fig.add_trace(go.Scatter(
                x=buy_signals['datetime'],
                y=buy_prices,
                mode='markers',
                marker=dict(color='green', size=10, symbol='triangle-up'),
                name='Buy Signal'
            ))
        if not sell_signals.empty:
            price_index = price_data.set_index('datetime')
            sell_prices = price_index.loc[sell_signals['datetime'], 'close']
            fig.add_trace(go.Scatter(
                x=sell_signals['datetime'],
                y=sell_prices,
                mode='markers',
                marker=dict(color='red', size=10, symbol='triangle-down'),
                name='Sell Signal'
            ))
    
    # Overlay trades if provided
    if trades is not None and not trades.empty:
        for idx, trade in trades.iterrows():
            fig.add_trace(go.Scatter(
                x=[trade['entry_time'], trade['exit_time']],
                y=[trade['entry_price'], trade['exit_price']],
                mode='lines+markers',
                line=dict(dash='dash', color='gray'),
                marker=dict(size=8),
                name=f"Trade {idx+1}"
            ))
    
    fig.update_layout(
        title="Price Chart with Signals and Trades",
        xaxis_title="Datetime",
        yaxis_title="Price"
    )
    return fig

def create_equity_curve_chart(equity: list, times: list) -> go.Figure:
    """
    Create an interactive equity curve chart.
    
    Parameters:
      equity: List of equity values.
      times: List of corresponding datetime values.
      
    Returns:
      A Plotly Figure object.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=times,
        y=equity,
        mode='lines+markers',
        name='Equity Curve',
        line=dict(color='purple')
    ))
    fig.update_layout(
        title="Equity Curve",
        xaxis_title="Time",
        yaxis_title="Equity"
    )
    return fig

if __name__ == "__main__":
    # Example usage with dummy data
    import numpy as np
    from datetime import datetime, timedelta
    
    dates = pd.date_range(start="2022-01-01", periods=100, freq='D')
    price_data = pd.DataFrame({
        'datetime': dates,
        'close': np.cumsum(np.random.randn(100)) + 100
    })
    
    signals = pd.DataFrame({
        'datetime': [dates[10], dates[30], dates[50], dates[70]],
        'signal': ['buy', 'sell', 'buy', 'sell']
    })
    
    trades = pd.DataFrame({
        'entry_time': [dates[10], dates[50]],
        'entry_price': [price_data.loc[price_data['datetime'] == dates[10], 'close'].values[0],
                        price_data.loc[price_data['datetime'] == dates[50], 'close'].values[0]],
        'exit_time': [dates[30], dates[70]],
        'exit_price': [price_data.loc[price_data['datetime'] == dates[30], 'close'].values[0],
                       price_data.loc[price_data['datetime'] == dates[70], 'close'].values[0]]
    })
    
    fig_price = create_price_chart(price_data, signals, trades)
    fig_price.show()
    
    equity = [100000, 100500, 100200, 100800, 101000]
    times = [dates[0], dates[10], dates[20], dates[30], dates[40]]
    fig_equity = create_equity_curve_chart(equity, times)
    fig_equity.show()

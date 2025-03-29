# ui/components/charts.py

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def plot_price_chart(price_data: pd.DataFrame, signals: pd.DataFrame = None):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=price_data.index,
        y=price_data["close"],
        mode='lines',
        name='Close Price'
    ))

    if signals is not None:
        for signal_name in signals.columns:
            signal_points = signals[signal_name].dropna()
            fig.add_trace(go.Scatter(
                x=signal_points.index,
                y=price_data.loc[signal_points.index, "close"],
                mode='markers',
                name=signal_name,
                marker=dict(symbol='x', size=8)
            ))

    fig.update_layout(title="Price Chart with Signals", xaxis_title="Time", yaxis_title="Price")
    st.plotly_chart(fig, use_container_width=True)


def plot_equity_curve(equity_curve: pd.Series):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=equity_curve.index,
        y=equity_curve.values,
        mode="lines",
        name="Equity"
    ))

    fig.update_layout(title="Equity Curve", xaxis_title="Date", yaxis_title="Equity")
    st.plotly_chart(fig, use_container_width=True)

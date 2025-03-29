# ui/pages/comparison_dashboard.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from reporting.comparison_dashboard import compare_equity_curves, compare_metrics

def load_saved_results():
    # Placeholder: Replace this with real loading logic
    st.info("Loading example saved runs...")
    return [
        {
            "strategy_name": "P9_Only",
            "metrics": {
                "Sharpe Ratio": 1.8,
                "Win Rate": 0.62,
                "Total Return": 0.25
            },
            "equity_curve": pd.Series([100, 105, 110, 112, 115], name="P9_Only")
        },
        {
            "strategy_name": "Combo_C13_P9",
            "metrics": {
                "Sharpe Ratio": 2.1,
                "Win Rate": 0.68,
                "Total Return": 0.31
            },
            "equity_curve": pd.Series([100, 108, 115, 120, 130], name="Combo_C13_P9")
        }
    ]

def display():
    st.title("📊 Strategy Comparison Dashboard")

    results = load_saved_results()

    equity_df = pd.concat([res["equity_curve"] for res in results], axis=1)
    compare_equity_curves(equity_df)

    st.markdown("---")

    metrics_df = pd.DataFrame([res["metrics"] for res in results], index=[res["strategy_name"] for res in results])
    compare_metrics(metrics_df)

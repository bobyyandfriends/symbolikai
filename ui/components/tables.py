# ui/components/tables.py

import streamlit as st
import pandas as pd

def show_trade_log(trades_df: pd.DataFrame):
    """
    Display trade log as a sortable table.
    """
    st.subheader("Trade Log")
    st.dataframe(trades_df.sort_values(by="entry_time").reset_index(drop=True))


def show_metrics_summary(metrics: dict):
    """
    Display strategy performance metrics.
    """
    st.subheader("Performance Summary")
    metrics_df = pd.DataFrame(metrics.items(), columns=["Metric", "Value"])
    st.table(metrics_df)

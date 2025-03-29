# ui/pages/signal_explorer.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from data.signal_loader import load_signals_from_file
from reporting.signal_heatmap import plot_signal_distribution

SIGNAL_DATA_PATH = "data/signals/"

def display():
    st.title("🔍 Signal Explorer")

    st.markdown("Use this tool to explore DeMark signal patterns across time, symbol, and type.")

    uploaded_file = st.file_uploader("Upload Signal File", type=["csv", "xlsx"])

    if uploaded_file is not None:
        st.success("Signal file uploaded.")
        df = load_signals_from_file(uploaded_file)

        signal_types = df["signal"].unique().tolist()
        selected_signals = st.multiselect("Filter by Signal Type", signal_types, default=signal_types[:3])

        date_range = st.date_input("Filter by Date Range", [])

        if selected_signals:
            filtered = df[df["signal"].isin(selected_signals)]

            if date_range and len(date_range) == 2:
                start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
                filtered = filtered[(filtered["timestamp"] >= start) & (filtered["timestamp"] <= end)]

            st.dataframe(filtered.head(50))

            if st.checkbox("Show Signal Frequency Heatmap"):
                fig = plot_signal_distribution(filtered)
                st.pyplot(fig)

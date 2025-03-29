#!/usr/bin/env python3
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def load_signal_data(file) -> pd.DataFrame:
    """
    Load signal data from an uploaded file.
    Supports CSV and Excel files.
    The function ensures that a datetime column (named either 'date' or 'datetime')
    is parsed as a datetime object and standardizes the column name to 'datetime'.
    """
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file)
        else:
            st.error("Unsupported file type. Please upload a CSV or Excel file.")
            return None

        # Rename 'date' column to 'datetime' if necessary
        if "date" in df.columns and "datetime" not in df.columns:
            df = df.rename(columns={"date": "datetime"})
        if "datetime" not in df.columns:
            st.error("The file must contain a 'date' or 'datetime' column.")
            return None

        # Parse datetime column
        df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
        df = df.dropna(subset=['datetime']).reset_index(drop=True)
        return df
    except Exception as e:
        st.error(f"Error loading signal file: {e}")
        return None

def plot_signal_heatmap(signals: pd.DataFrame):
    """
    Create a heatmap of signal frequency by day of week and hour of day.
    The function extracts the day (0=Monday,...,6=Sunday) and hour from the 'datetime' column,
    builds a pivot table of counts, and uses seaborn to plot the heatmap.
    """
    df = signals.copy()
    df['day_of_week'] = df['datetime'].dt.dayofweek
    df['hour'] = df['datetime'].dt.hour

    pivot = df.pivot_table(index='day_of_week', columns='hour', values='signal', aggfunc='count', fill_value=0)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(pivot, annot=True, fmt="d", cmap="YlGnBu", ax=ax)
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Day of Week (0=Mon, 6=Sun)")
    ax.set_title("Signal Frequency Heatmap")
    plt.tight_layout()
    return fig

def main():
    st.title("Signal Explorer")
    st.write("Upload your DeMark signal data to explore signal patterns.")

    file = st.file_uploader("Upload Signal Data (CSV or Excel)", type=["csv", "xls", "xlsx"])

    if file is not None:
        signals = load_signal_data(file)
        if signals is not None:
            st.success("Signal data loaded successfully.")
            st.write("### Signal Data Preview")
            st.dataframe(signals.head())

            if st.checkbox("Show full data"):
                st.dataframe(signals)

            st.write("### Signal Frequency Heatmap")
            heatmap_fig = plot_signal_heatmap(signals)
            st.pyplot(heatmap_fig)
    else:
        st.info("Please upload a signal file to begin exploration.")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
import sys

# Dynamically add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# Import required functions and classes from your modules
from strategies.strategy_loader import load_strategy
from data.pricing_loader import load_price_data
from backtest.backtester import run_backtest
from reporting.comparison_dashboard import compare_equity_curves, compare_metrics

def comparison_dashboard_page():
    st.title("Comparison Dashboard")
    st.write("Compare multiple strategy backtests side by side using the same historical price data.")
    
    st.sidebar.header("Backtest Configuration")
    price_file = st.sidebar.file_uploader("Upload Price Data (CSV)", type=["csv"])
    
    if price_file is not None:
        try:
            price_data = pd.read_csv(price_file, parse_dates=["datetime"])
            st.success("Price data loaded successfully.")
            st.write("### Price Data Preview")
            st.dataframe(price_data.head())
        except Exception as e:
            st.error(f"Error loading price data: {e}")
            st.stop()
    else:
        st.info("Please upload price data to proceed.")
        st.stop()
    
    available_strategies = ["SimpleStrategy", "DemarkPerfectionStrategy", "ComboStrategyExample"]
    selected_strategies = st.sidebar.multiselect("Select Strategies to Compare", available_strategies, default=available_strategies)
    
    initial_capital = st.sidebar.number_input("Initial Capital", min_value=10000, value=100000, step=10000)
    
    if st.button("Run Comparison Backtests"):
        results_list = []
        for strat_name in selected_strategies:
            strategy = load_strategy(strat_name)
            # Generate signals using the strategy's logic
            signals = strategy.generate_signals(price_data)
            config = {"initial_capital": initial_capital}
            results = run_backtest(strategy, price_data, signals, config)
            results_list.append(results)
        
        if results_list:
            st.subheader("Equity Curves Comparison")
            # compare_equity_curves should plot and return a figure; here we capture that figure.
            fig_eq = compare_equity_curves(results_list)
            st.pyplot(fig_eq)
            
            st.subheader("Performance Metrics Comparison")
            metrics_df = compare_metrics(results_list)
            st.dataframe(metrics_df)
        else:
            st.error("No backtest results to compare.")

if __name__ == "__main__":
    comparison_dashboard_page()

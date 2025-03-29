#!/usr/bin/env python3
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Import functions and classes from your project modules
from data.pricing_loader import load_price_data
from data.signal_loader import load_signals_from_file, normalize_signals
from strategies.strategy_loader import load_strategy
from backtest.backtester import run_backtest

def strategy_tester_page():
    st.title("Strategy Tester")
    
    # Sidebar inputs for symbol and timeframe
    st.sidebar.header("Backtest Configuration")
    symbol = st.sidebar.text_input("Enter Symbol", "AAPL")
    timeframe = st.sidebar.selectbox("Select Timeframe", ("daily", "240min"))
    
    # Strategy selection
    strategy_option = st.sidebar.selectbox("Select Strategy", 
                                           ("SimpleStrategy", "DemarkPerfectionStrategy", "ComboStrategyExample"))
    
    # File uploader for signal data (optional)
    signal_file = st.sidebar.file_uploader("Upload Signal Data (CSV or Excel)", type=["csv", "xlsx"])
    if signal_file is not None:
        try:
            signal_df = load_signals_from_file(signal_file)
            signal_df = normalize_signals(signal_df)
            st.sidebar.success("Signal data loaded successfully.")
        except Exception as e:
            st.sidebar.error(f"Error loading signal data: {e}")
            signal_df = None
    else:
        signal_df = None
    
    # Load price data from CSV file(s)
    try:
        price_data = load_price_data(symbol, timeframe)
        st.success("Price data loaded successfully.")
    except Exception as e:
        st.error(f"Error loading price data: {e}")
        st.stop()
    
    # Run Backtest button
    if st.button("Run Backtest"):
        st.subheader("Running Backtest...")
        strategy = load_strategy(strategy_option)
        # If no external signal data is provided, generate signals using the strategy's logic
        if signal_df is None:
            signals = strategy.generate_signals(price_data)
        else:
            signals = strategy.generate_signals(price_data, signal_df)
        
        config = {"initial_capital": 100000}
        results = run_backtest(strategy, price_data, signals, config)
        
        # Display Metrics
        st.subheader("Backtest Metrics")
        st.write(results["metrics"])
        
        # Display Trade Log
        st.subheader("Trade Log")
        st.dataframe(results["trades"])
        
        # Plot Equity Curve if trades exist
        if not results["trades"].empty:
            equity = [config["initial_capital"]]
            times = [results["trades"].iloc[0]["entry_time"]]
            for _, trade in results["trades"].iterrows():
                equity.append(equity[-1] + trade["profit"])
                times.append(trade["exit_time"])
            
            fig_eq, ax_eq = plt.subplots(figsize=(8, 4))
            ax_eq.plot(times, equity, marker="o", color="purple")
            ax_eq.set_title("Equity Curve")
            ax_eq.set_xlabel("Time")
            ax_eq.set_ylabel("Equity")
            st.pyplot(fig_eq)
        else:
            st.info("No trades were executed during the backtest.")

if __name__ == "__main__":
    strategy_tester_page()

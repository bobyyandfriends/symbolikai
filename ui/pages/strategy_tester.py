# ui/pages/strategy_tester.py

import streamlit as st
from strategies.strategy_loader import load_strategy
from data.pricing_loader import load_price_data
from data.signal_loader import load_signals_from_file
from backtest.backtester import run_backtest
from reporting.visualizer import plot_strategy_summary
from reporting.equity_curve import plot_equity_curve
from reporting.trade_report import print_performance_summary

def display():
    st.title("🧪 Strategy Tester")

    st.markdown("Select a strategy and configure parameters to run a backtest.")

    symbol = st.text_input("Symbol", value="AAPL")
    timeframe = st.selectbox("Timeframe", ["daily", "240min", "60min"], index=0)
    strategy_name = st.selectbox("Strategy", ["PerfectionStrategy", "ComboStrategyExample"])

    capital = st.number_input("Initial Capital", value=100000)
    slippage = st.slider("Slippage (%)", 0.0, 0.5, 0.1)

    uploaded_signal_file = st.file_uploader("Upload Signal File", type=["csv", "xlsx"])

    if st.button("Run Backtest") and uploaded_signal_file:
        st.success("Running backtest...")
        strategy_class = load_strategy(strategy_name)
        strategy = strategy_class()

        price_data = load_price_data(symbol, timeframe)
        signal_data = load_signals_from_file(uploaded_signal_file)

        results = run_backtest(strategy, price_data, signal_data, {
            "initial_capital": capital,
            "slippage_pct": slippage,
            "side": "long"
        })

        st.subheader("📈 Strategy Summary")
        plot_strategy_summary(price_data, results["trades"], signal_data)

        st.subheader("📊 Equity Curve")
        plot_equity_curve(results["trades"])

        st.subheader("📋 Performance Metrics")
        print_performance_summary(results["metrics"])

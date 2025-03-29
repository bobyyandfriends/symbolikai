# main.py

from data.pricing_loader import load_price_data
from data.signal_loader import load_signals_from_file
from strategies.demark_perfection_strategy import PerfectionStrategy
from backtest.backtester import run_backtest
from reporting.visualizer import plot_strategy_summary
from reporting.equity_curve import plot_equity_curve
from reporting.trade_report import print_performance_summary

def main():
    symbol = "AAPL"
    timeframe = "daily"

    print(f"Loading price and signal data for {symbol}...")
    price_data = load_price_data(symbol, timeframe)
    signal_data = load_signals_from_file(f"data/signals/{symbol}_signals.csv")

    strategy = PerfectionStrategy()
    strategy.generate_trades(price_data, signal_data)

    results = run_backtest(strategy, price_data, signal_data, config={
        "initial_capital": 100000,
        "slippage_pct": 0.001,
        "side": "long"
    })

    print_performance_summary(results["metrics"])
    plot_strategy_summary(price_data, results["trades"], signal_data)
    plot_equity_curve(results["trades"])

if __name__ == "__main__":
    main()

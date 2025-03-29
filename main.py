#!/usr/bin/env python3
import argparse
import sys
from utils.config_loader import load_config
from data.pricing_loader import load_price_data
from data.signal_loader import load_signals_from_file, normalize_signals
from strategies.strategy_loader import load_strategy
from backtest.backtester import run_backtest
import pandas as pd

def run_cli_backtest(args):
    """
    Runs a backtest from the command line.
    It loads the configuration, price data, (optional) external signal data, and the chosen strategy,
    then executes the backtest and prints the metrics and trade log.
    """
    # Load configuration from YAML (if available)
    try:
        config = load_config(args.config)
    except Exception as e:
        print(f"Error loading config: {e}")
        config = {}
    
    # Load historical price data
    try:
        price_data = load_price_data(args.symbol, args.timeframe)
    except Exception as e:
        print(f"Error loading price data for symbol {args.symbol} with timeframe {args.timeframe}: {e}")
        sys.exit(1)
    
    # Load external signal data if provided
    if args.signal_file:
        try:
            # Here we assume the signal file is a local file path
            signal_df = load_signals_from_file(args.signal_file)
            signal_df = normalize_signals(signal_df)
        except Exception as e:
            print(f"Error loading signal data: {e}")
            signal_df = None
    else:
        signal_df = None

    # Load the selected strategy
    try:
        strategy = load_strategy(args.strategy)
    except Exception as e:
        print(f"Error loading strategy '{args.strategy}': {e}")
        sys.exit(1)
    
    # Generate signals using strategy logic (or overlay external signals if provided)
    if signal_df is None:
        signals = strategy.generate_signals(price_data)
    else:
        signals = strategy.generate_signals(price_data, signal_df)
    
    # Use the configuration; ensure a default initial capital if not provided
    config.setdefault("initial_capital", 100000)
    results = run_backtest(strategy, price_data, signals, config)
    
    # Print metrics and trades to the console
    print("=== Backtest Metrics ===")
    for key, value in results["metrics"].items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    
    print("\n=== Trade Log ===")
    if not results["trades"].empty:
        print(results["trades"].to_string(index=False))
    else:
        print("No trades were executed.")
        
def run_ui():
    """
    Launches the interactive UI.
    """
    from ui.app import main as ui_main
    ui_main()

def main():
    parser = argparse.ArgumentParser(description="SymbolikAI Trading Intelligence System")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Subparser for running a backtest
    parser_backtest = subparsers.add_parser("backtest", help="Run a backtest from the command line")
    parser_backtest.add_argument("--config", type=str, default="config.yaml", help="Path to configuration file")
    parser_backtest.add_argument("--symbol", type=str, default="AAPL", help="Trading symbol")
    parser_backtest.add_argument("--timeframe", type=str, default="daily", help="Price data timeframe (e.g., daily, 240min)")
    parser_backtest.add_argument("--strategy", type=str, default="SimpleStrategy", help="Strategy name to use")
    parser_backtest.add_argument("--signal_file", type=str, help="Path to external signal data file (CSV or Excel)")
    
    # Subparser for launching the UI
    parser_ui = subparsers.add_parser("ui", help="Launch the interactive UI")
    
    # Parse arguments and run the appropriate command
    args = parser.parse_args()
    
    if args.command == "backtest":
        run_cli_backtest(args)
    elif args.command == "ui":
        run_ui()
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()

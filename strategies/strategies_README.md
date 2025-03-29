
# strategies/

## Purpose
The `strategies/` folder contains all logic related to trade entry and exit strategies. These strategies interpret DeMark signals, technical indicators, and potentially machine learning outputs to decide when to enter and exit trades. Each strategy is modular and pluggable, supporting rapid experimentation, backtesting, and deployment.

## Folder Structure
- `__init__.py`: Initializes the folder as a Python package for clean imports.
- `base_strategy.py`: Abstract base class defining the interface and shared logic for all strategy implementations.
- `rule_engine.py`: Utility for evaluating logical rules defined as Python dictionaries. Used by rule-based strategies.
- `strategy_loader.py`: Dynamically loads strategy classes by name for runtime selection.
- `demark_perfection_strategy.py`: Strategy that uses the Perfection9 signal for long/short entries with optional RSI filters.
- `combo_strategy_example.py`: Combines multiple signals like C13Up, TDST, and indicators like momentum for advanced strategies.

## How Strategies Work
Each strategy implements the `Strategy` interface and consists of:
- `apply_indicators`: Computes TA indicators to enrich the price data.
- `generate_signals`: Applies logic or rules to identify entry/exit points.
- `generate_trades`: Converts signals into Trade objects with position size, side, and stop-loss/profit target.

## Strategy Design Philosophy
- **Modular**: Easily swap in new strategies without changing backtester code.
- **Composable**: Combine signals and rules from various sources (DeMark, indicators, ML).
- **Explainable**: Most logic is transparent and rule-based, facilitating interpretation.
- **ML-Ready**: Strategies may use ML predictions for scoring or ranking signals.

## Adding a New Strategy
1. Create a new file like `my_custom_strategy.py`.
2. Inherit from `Strategy` and implement required methods.
3. Register it in `strategy_loader.py` for easy import.

## Usage Example
```python
from strategies.demark_perfection_strategy import PerfectionStrategy
strategy = PerfectionStrategy()
price_data = load_price_data("AAPL", "daily")
signals = load_signals("AAPL")
trades = strategy.generate_trades(price_data, signals)
```

## Future Enhancements
- Strategy configuration via YAML/JSON
- Hyperparameter tuning for strategies
- Time-of-day and macro filters
- More ML-augmented strategy classes

# Backtest Module

The `backtest/` folder contains all the core logic related to running historical backtests for your trading strategies. It simulates trades using signal data and price data and calculates key performance metrics and visualizations. This is the heart of evaluating strategy performance before live trading.

---

## 📁 File Descriptions

### `__init__.py`
Marks the `backtest` folder as a Python package. Contains no logic.

---

### `backtester.py`
**Purpose:**  
Orchestrates the full backtest. Takes a strategy, historical data, and parameters, and returns trade results and performance.

**Key Functions:**
- `run_backtest(strategy, price_data, signal_data, config)` – Runs a full simulation and returns trades, metrics, equity curve, etc.
- `simulate_trades(entry_signals, exit_signals, price_data, capital)` – Converts entry/exit signals into executable trades, manages capital, and tracks PnL.

---

### `trade.py`
**Purpose:**  
Defines the `Trade` class that represents a single executed trade.

**Attributes:**
- Entry/exit price and time
- Side (long or short)
- Signal name and confidence (optional)
- PnL and return

**Functions:**
- `calculate_pnl()`
- `apply_slippage()`
- `to_dict()`

---

### `metrics.py`
**Purpose:**  
Calculates quantitative performance metrics from the executed trades.

**Metrics Include:**
- Win rate
- Total return
- Max drawdown
- Sharpe ratio
- Profit factor
- Average holding time

---

### `plotter.py`
**Purpose:**  
Visualizes the results of the backtest using matplotlib or Plotly.

**Plots:**
- Entry and exit points on price chart
- Equity curve over time
- Optional: drawdown and signal overlays

---

### `context.py` (Optional)
**Purpose:**  
Stores live simulation state during the backtest, such as current equity, cash, and active trades. Useful for more complex multi-symbol or multi-account simulations.

---

## ✅ Key Features
- Supports **long and short** trades
- Tracks **capital**, **PnL**, and **slippage**
- Works with **signal data** from `data/` layer
- Outputs trades, equity, and metrics
- Easily pluggable with any strategy from the `strategies/` module

---

## 🔮 Future Enhancements
- Add commissions modeling
- Add multi-symbol batch backtesting
- Integrate benchmark performance comparison
- Optionally include intraday latency/slippage simulation

---

## 🧠 Best Practices
- Keep strategy logic separated in `strategies/`
- Use consistent timestamps between signal and price data
- Track capital per-trade for realistic performance metrics

---

## 📎 Usage Example
```python
from strategies.demark_perfection_strategy import PerfectionStrategy
from backtest.backtester import run_backtest
from data.pricing_loader import load_price_data
from data.signal_loader import load_signals

strategy = PerfectionStrategy()
price_data = load_price_data("AAPL", "daily")
signals = load_signals("AAPL")

results = run_backtest(strategy, price_data, signals, config={
    "initial_capital": 100000,
    "slippage_pct": 0.001,
    "side": "long"
})
```

---

This module is designed to be **modular, transparent, and extensible**—a robust engine for evaluating the real-world performance of trading ideas.
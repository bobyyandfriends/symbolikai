
# 📊 reporting/

The `reporting/` module provides tools for visualizing, interpreting, and exporting strategy backtest results. This layer sits at the intersection of analytics and presentation, offering visual insight into trading performance, signal behavior, and equity evolution. It is a critical part of the research loop, allowing quick diagnosis and comparative analysis of strategies.

---

## 📁 File Overview

### `visualizer.py`
Plots a comprehensive strategy view by overlaying price charts with entries, exits, and signal points.

- `plot_strategy_summary(price_data, trades, signals)`: Full chart with entry/exit markers and signal overlays.
- `plot_overlay_with_indicators(price_data, indicators)`: Price chart plus RSI, Bollinger Bands, etc.

### `equity_curve.py`
Visualizes account value and drawdowns over time.

- `plot_equity_curve(trades)`: Line chart of portfolio growth.
- `plot_drawdowns(trades)`: Highlights periods of equity decline.

### `signal_heatmap.py`
Explores signal behavior across dimensions like time, frequency, and correlation.

- `plot_signal_distribution(signals)`: Signal frequency by time-of-day or day-of-week.
- `plot_indicator_interaction_matrix()`: Shows how indicators interact with different signals.

### `trade_report.py`
Generates readable trade logs and performance summaries.

- `generate_trade_log(trades)`: DataFrame of entry/exit, PnL, duration, etc.
- `print_performance_summary(metrics_dict)`: Outputs key metrics like Sharpe, win rate, drawdown.
- `export_summary_to_txt(...)`, `export_trades_to_csv(...)`: Optional exports.

### `comparison_dashboard.py`
Compares multiple strategy runs side by side.

- `compare_equity_curves(results_list)`
- `compare_metrics(results_list)`: Side-by-side view of strategy KPIs.

---

## 🧠 Design Principles

- Modular: Each file handles one kind of visualization or report.
- Notebook-friendly: Works seamlessly with Jupyter and Streamlit.
- Extensible: Can plug into UI, dashboard, or reporting APIs.

---

## 🧪 Use Cases

- Analyze equity growth, volatility, and drawdowns
- Visualize performance against different market conditions
- Compare multiple strategies using consistent metrics
- Export strategy results for external reporting

---

## 🔄 Dependencies

- `matplotlib`, `seaborn`, `plotly` for plotting
- `pandas` for tabular manipulation

---

## 🧰 Future Enhancements

- Add interactive charts with Plotly/Dash
- Extend to include risk-adjusted metrics (Sortino, Omega)
- Multi-symbol equity curve tracking
- Cloud dashboard for real-time reporting

---

## 🧭 Example

```python
from reporting.visualizer import plot_strategy_summary
from reporting.equity_curve import plot_equity_curve
from reporting.trade_report import print_performance_summary

plot_strategy_summary(price_data, trades, signals)
plot_equity_curve(trades)
print_performance_summary(metrics)
```

> The `reporting/` module closes the loop between strategy and insight. It transforms raw trades into stories, mistakes into lessons, and signals into confidence.

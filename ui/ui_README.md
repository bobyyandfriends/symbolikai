# 🖥️ ui/

The `ui/` folder contains the Streamlit-based user interface for the SymbolikAI system. This interactive UI layer provides full control and visibility over your strategies, backtests, ML models, and signal behavior.

It transforms the system from a developer-only toolkit into a trading research platform that anyone can use to run tests, explore signals, and view performance dashboards.

---

## 📁 Folder Structure

```
ui/
├── __init__.py
├── app.py
├── pages/
│   ├── strategy_tester.py
│   ├── signal_explorer.py
│   ├── model_trainer.py
│   └── comparison_dashboard.py
└── components/
    ├── charts.py
    └── tables.py
```

---

## 🧭 File Descriptions

### ✅ `ui/app.py`
- **Purpose**: Entry point for the Streamlit app.
- **What It Does**:
  - Manages navigation between pages.
  - Loads shared settings and session state.
  - Central launch point for the UI.

---

### ✅ `ui/pages/strategy_tester.py`
- **Purpose**: Lets users select a strategy, symbol, and run a backtest interactively.
- **Features**:
  - Dropdowns for strategy, symbol, timeframe
  - Capital and slippage inputs
  - Real-time trade charts, equity curves, and performance summaries

---

### ✅ `ui/pages/signal_explorer.py`
- **Purpose**: Explore and visualize historical DeMark signals.
- **Features**:
  - Signal filters (e.g., Perfection9Up, C13)
  - Timeframe/date range pickers
  - Signal overlays on price charts
  - Heatmaps of signal frequency

---

### ✅ `ui/pages/model_trainer.py`
- **Purpose**: Train, evaluate, and save machine learning models from the UI.
- **Features**:
  - Model selection interface
  - Train/test split config
  - Display of training metrics and charts
  - Button to save/export models

---

### ✅ `ui/pages/comparison_dashboard.py`
- **Purpose**: Compare multiple strategy runs side by side.
- **Features**:
  - Load/run saved strategies
  - Equity curves on one plot
  - Tabular metrics comparison (Sharpe, PnL, Win Rate)

---

### ✅ `ui/components/charts.py`
- **Purpose**: Reusable chart rendering functions.
- **Includes**:
  - Price + signal overlays
  - Equity curves
  - Indicator overlays

---

### ✅ `ui/components/tables.py`
- **Purpose**: Reusable table formatting utilities.
- **Includes**:
  - Trade logs
  - Performance summaries
  - Signal statistics

---

## 🛠️ Running the UI

```bash
streamlit run ui/app.py
```

You’ll need:
- Data ingested and saved in `/data/`
- At least one strategy implemented
- Backtest engine functional

---

## 🚀 Future Enhancements

- Strategy builder UI with drag-and-drop logic blocks
- Live data feed for real-time testing
- Model explainability (SHAP values, feature importance)
- User-configurable dashboards
- Authentication (for multi-user cloud deployment)

---

The `ui/` folder brings the SymbolikAI ecosystem to life with rich interactivity, full control, and visual exploration. It's the command center for your entire research process.
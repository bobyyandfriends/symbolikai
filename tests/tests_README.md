# 📁 tests/

The `tests/` folder contains unit tests and integration tests that ensure the correctness, reliability, and consistency of all components in the SymbolikAI project.

Each test module corresponds to a different part of the architecture, providing test coverage for the strategy logic, data ingestion, machine learning pipeline, and backtesting engine.

---

## 🧪 Files Overview

### ✅ `test_backtester.py`
- **Purpose:** Verifies core functionality of the backtesting engine.
- **What It Tests:**
  - Execution of strategies on sample data.
  - Trade lifecycle (entry/exit).
  - Correctness of calculated metrics (win rate, Sharpe, PnL, etc.).
- **Example Tests:**
  - `test_run_backtest_returns_valid_structure`
  - `test_trade_entry_and_exit_logic`

---

### ✅ `test_data.py`
- **Purpose:** Validates data ingestion, formatting, and storage utilities.
- **What It Tests:**
  - Reading and writing of price and signal data.
  - Deduplication of signals.
  - File path generation and CSV I/O logic.
- **Example Tests:**
  - `test_load_price_data`
  - `test_save_and_load_signal_file`

---

### ✅ `test_ml.py`
- **Purpose:** Tests machine learning feature engineering, model training, and inference.
- **What It Tests:**
  - Feature generation from price and signal data.
  - Model training with test labels.
  - Prediction and scoring mechanics.
- **Example Tests:**
  - `test_generate_ml_features`
  - `test_model_training_pipeline`

---

### ✅ `test_strategy.py`
- **Purpose:** Tests individual strategy logic and rule evaluation.
- **What It Tests:**
  - Entry/exit signal generation from strategies.
  - Rule-based filtering logic (e.g., RSI < 30).
  - Indicator application and integration with signals.
- **Example Tests:**
  - `test_strategy_generates_signals`
  - `test_apply_indicators_in_strategy`

---

## 🧪 Testing Philosophy

- 📦 **Modular**: Each component has its own test file.
- 🔁 **Repeatable**: Fixtures and mock data allow rerunning tests without internet access.
- 🧰 **Expandable**: Add new tests as features evolve (e.g., testing Streamlit UI with `pytest-streamlit` or using `pytest-dash`).

---

## 🛠️ Running Tests

From the root of the project:
```bash
pytest tests/
```

Or run a single file:
```bash
pytest tests/test_data.py
```

---

## ✅ Future Enhancements

- Add test coverage reports with `pytest-cov`
- Integrate with GitHub Actions for continuous integration (CI)
- Write regression tests for ML model performance
- Add load testing for real-time data ingestion and strategy response

---

This test suite ensures that SymbolikAI behaves as expected and accelerates safe refactoring and experimentation.

# Notebooks

This folder contains interactive Jupyter Notebooks used for exploratory data analysis (EDA), prototyping trading features, testing machine learning models, and analyzing signal behaviors. These notebooks act as a sandbox environment to iterate quickly before implementing ideas in the main codebase.

## 📘 Contents

### 1. `feature_prototype.ipynb`
- Purpose: Test out new feature engineering ideas before integrating them into the ML pipeline.
- Example Features Explored:
  - Rolling volatility metrics
  - RSI and Momentum bands
  - Signal stacking logic
- Use Cases:
  - Visualize indicator interactions
  - Plot feature distributions
  - Create candidate features for model training

### 2. `model_tester.ipynb`
- Purpose: Train and evaluate machine learning models (XGBoost, RandomForest, etc.) in isolation.
- Workflow:
  1. Load labeled trade data
  2. Split into train/test sets
  3. Train model and evaluate accuracy, precision, recall, AUC
  4. Display feature importance
- Visualization Tools:
  - Confusion matrices
  - SHAP or permutation importance
  - Prediction distribution

### 3. `signal_analysis.ipynb`
- Purpose: Analyze the behavior of individual signals across symbols and timeframes.
- Typical Analyses:
  - Frequency distribution by signal type
  - Signal alignment with price direction
  - Pre- and post-signal return analysis
- Useful for:
  - Validating reliability of proprietary signals
  - Identifying best filters or combinations
  - Debugging false signals or failure cases

## 💡 Development Philosophy

Jupyter Notebooks allow for fast iteration and visualization when researching new ideas. These notebooks are **not production code**, but rather scratchpads for experimentation. Once logic is proven here, it should be ported to the appropriate module in the codebase (`ml/`, `data/`, `strategies/`, etc.).

## ✅ Best Practices

- Always comment your steps for reproducibility.
- Use lightweight data for initial tests before scaling up.
- Tag successful experiments in markdown cells for easy future reference.
- Consider exporting charts and metrics into the `reporting/` layer.

## 📎 Dependencies

Ensure you have the following packages available in your Jupyter environment:
- `pandas`
- `matplotlib`
- `seaborn`
- `xgboost`
- `sklearn`
- `shap` (optional, if installed)

## 🚀 Tips

- Clone new notebooks from a template to maintain consistency.
- Backtest promising strategies offline before committing.
- Use `%matplotlib inline` for inline chart display.

---

📁 This directory empowers fast experimentation—feel free to fork and test wild ideas!

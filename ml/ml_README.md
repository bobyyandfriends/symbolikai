
# ML Module

The `ml/` directory contains all logic related to machine learning components of the SymbolikAI system.
These components allow the system to learn from historical trades, detect regimes, reflect on performance, and dynamically adjust behavior.

## Contents

### `environment_classifier.py`
This module provides tools to detect the current market environment or "regime." It is used to inform strategies about the prevailing conditions.

**Key Features:**
- Classifies market environment using clustering or ML classification.
- Can use technical indicators (e.g., volatility, trend strength) as features.
- Provides labels like "trending", "choppy", "volatile", "calm", etc.

### `meta_modeling.py`
This module trains meta-models to learn when a base strategy or signal is likely to succeed or fail.

**Key Features:**
- Learns meta-labels (outcome of trades or conditions under which signals work).
- Can use signal metadata and feature context.
- Enhances strategy selection and model stacking.

### `self_reflection.py`
A novel component that attempts to assess past decisions and performance to generate suggestions or commentary.

**Key Features:**
- Analyzes trade logs to find patterns in wins/losses.
- Detects biases or recurring mistakes.
- Generates reasoning-style commentary (e.g., "RSI overbought at entry = lower win rate").

## Design Philosophy

- Modular ML Pipelines: Each script is self-contained but interoperable with the strategy and backtesting layers.
- Compatible with Scikit-learn, XGBoost, and other ML libraries.
- Feature engineering is often tied to trading context (momentum, volatility, etc.).

## Example Use Case

Train a meta-model to filter trades:

```python
from ml.meta_modeling import train_meta_model, predict_with_model
from data.data_store import load_df_csv

X = load_df_csv("features.csv")
y = load_df_csv("labels.csv")

model = train_meta_model(X, y)
predictions = predict_with_model(model, X)
```

## Future Enhancements

- Add SHAP/interpretability to explain model decisions.
- Integrate confidence scoring and feature importance feedback into UI.
- Add model versioning and model registry support.

## Dependencies

- scikit-learn
- xgboost (or lightgbm)
- pandas
- numpy

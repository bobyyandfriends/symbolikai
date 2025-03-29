#!/usr/bin/env python3
import pytest
import pandas as pd
import numpy as np
from ml.model_training import generate_features, train_model
from ml.label_generation import generate_labels, filter_valid_labels
from ml.environment_classifier import EnvironmentClassifier

@pytest.fixture
def dummy_price_data_ml():
    dates = pd.date_range(start="2022-01-01", periods=100, freq="D")
    np.random.seed(42)
    prices = np.cumsum(np.random.randn(100)) + 100
    data = pd.DataFrame({
        "datetime": dates,
        "close": prices,
        "high": prices + np.random.rand(100),
        "low": prices - np.random.rand(100)
    })
    data["rsi"] = 50 + 10 * np.sin(np.linspace(0, 10, 100))
    data["sma"] = data["close"].rolling(window=10, min_periods=10).mean()
    data = data.dropna().reset_index(drop=True)
    return data

@pytest.fixture
def dummy_signals_ml(dummy_price_data_ml):
    return pd.DataFrame({
        "datetime": dummy_price_data_ml["datetime"],
        "signal": ["buy" if i % 2 == 0 else "sell" for i in range(len(dummy_price_data_ml))]
    })

def test_generate_features(dummy_price_data_ml, dummy_signals_ml):
    features_df = generate_features(dummy_price_data_ml, dummy_signals_ml)
    for col in ["rsi", "sma", "momentum", "signal_binary"]:
        assert col in features_df.columns
    assert "target" in features_df.columns

def test_train_model(dummy_price_data_ml, dummy_signals_ml):
    features_df = generate_features(dummy_price_data_ml, dummy_signals_ml)
    model = train_model(features_df)
    assert model is not None
    assert hasattr(model, "predict")

def test_generate_labels(dummy_price_data_ml):
    labeled_df = generate_labels(dummy_price_data_ml, future_window=5, profit_threshold=0.02, loss_threshold=-0.01)
    assert "label" in labeled_df.columns
    valid_df = filter_valid_labels(labeled_df)
    assert valid_df["label"].isna().sum() == 0

def test_environment_classifier(dummy_price_data_ml):
    from ml.environment_classifier import EnvironmentClassifier
    classifier = EnvironmentClassifier(n_clusters=3)
    classifier.fit(dummy_price_data_ml)
    preds = classifier.predict(dummy_price_data_ml)
    features = classifier.extract_features(dummy_price_data_ml)
    assert isinstance(preds, pd.Series)
    assert len(preds) == len(features)

if __name__ == "__main__":
    pytest.main()

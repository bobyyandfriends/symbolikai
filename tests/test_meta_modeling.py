#!/usr/bin/env python3
import pytest
import pandas as pd
import numpy as np
from ml.meta_modeling import MetaModel
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
import os

@pytest.fixture
def dummy_classification_data():
    X, y = make_classification(n_samples=200, n_features=5, random_state=42)
    X = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(5)])
    y = pd.Series(y)
    return X, y

def test_meta_model_build_train_predict_evaluate(tmp_path, dummy_classification_data):
    X, y = dummy_classification_data
    # Define base models
    base_models = {
        "lr": LogisticRegression(random_state=42, max_iter=200),
        "dt": DecisionTreeClassifier(random_state=42)
    }
    # Use temporary file path for saving the meta-model
    model_save_path = tmp_path / "meta_model_test.pkl"
    meta = MetaModel(mode="hard_voting", save_path=str(model_save_path))
    meta.build(base_models)
    meta.train(X, y)
    
    # Evaluate the model
    accuracy = meta.evaluate(X, y)
    assert 0.0 <= accuracy <= 1.0, "Accuracy should be between 0 and 1."
    
    # Check predictions shape
    predictions = meta.predict(X)
    assert predictions.shape[0] == X.shape[0], "Number of predictions must match number of samples."
    
    # Verify that the model file has been created
    assert os.path.exists(str(model_save_path)), "Meta-model file not found."

if __name__ == "__main__":
    pytest.main()

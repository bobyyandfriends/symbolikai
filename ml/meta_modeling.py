# ml/meta_modeling.py

import pandas as pd
import numpy as np
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from joblib import dump, load


class MetaModel:
    """
    Meta-model that combines multiple base model predictions (stacking, voting).
    Supports training and inference.
    """

    def __init__(self, mode="hard_voting", save_path="ml/models/meta_model.pkl"):
        """
        mode: "hard_voting", "soft_voting", or "stacking"
        """
        self.mode = mode
        self.save_path = save_path
        self.model = None

    def build(self, base_models: dict):
        """
        Create the meta-model ensemble.
        base_models: dict of {model_name: sklearn-compatible model}
        """
        estimators = [(name, model) for name, model in base_models.items()]
        if self.mode == "hard_voting":
            self.model = VotingClassifier(estimators=estimators, voting="hard")
        elif self.mode == "soft_voting":
            self.model = VotingClassifier(estimators=estimators, voting="soft")
        elif self.mode == "stacking":
            self.model = VotingClassifier(estimators=estimators, voting="soft")  # Placeholder
            # Replace with sklearn's StackingClassifier if stacking logic needed
        else:
            raise ValueError("Invalid meta-model mode")

    def train(self, X: pd.DataFrame, y: pd.Series):
        """
        Fit the meta-model using feature set X and target y.
        """
        if self.model is None:
            raise RuntimeError("Meta-model has not been built. Call .build() first.")
        self.model.fit(X, y)
        dump(self.model, self.save_path)

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Generate predictions using the meta-model.
        """
        if self.model is None:
            self.model = load(self.save_path)
        return self.model.predict(X)

    def evaluate(self, X: pd.DataFrame, y_true: pd.Series) -> float:
        """
        Evaluate prediction accuracy.
        """
        y_pred = self.predict(X)
        return accuracy_score(y_true, y_pred)

#!/usr/bin/env python3
"""
meta_modeling.py

An enhanced meta-modeling framework that supports different ensemble modes:
  - Hard voting
  - Soft voting
  - Stacking (StackingClassifier)

It can incorporate synergy signals or columns at the meta-level if needed. 
Trains, saves, loads, and evaluates the meta-model. Example usage:

base_models = {
    "dt": DecisionTreeClassifier(...),
    "svc": SVC(probability=True, ...),
    "lr": LogisticRegression(...)
}
X, y = ... # your data
meta = MetaModel(mode="stacking", save_path="models/meta_model.pkl", use_synergy=True)
meta.build(base_models)
meta.train(X, y)
acc = meta.evaluate(X, y)
"""

import os
import pandas as pd
import numpy as np
from typing import Dict
from sklearn.ensemble import VotingClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split, cross_val_score
from joblib import dump, load

class MetaModel:
    """
    Meta-model that combines predictions from multiple base models (estimators).
    Offers:
      - Hard voting
      - Soft voting
      - Stacking

    Also can incorporate synergy columns if self.use_synergy is True.
      => synergy columns from X can remain, or you can do weighting. 
         For instance, you can do synergy weighting in train(...) if you want advanced logic.

    Typical usage:
      meta = MetaModel(mode="stacking", save_path="meta_model.pkl", use_synergy=True)
      meta.build(base_models)
      meta.train(X, y)
      meta.evaluate(X_test, y_test)
      # meta.predict(X_new)
    """

    def __init__(self,
                 mode: str = "hard_voting",
                 save_path: str = "ml/models/meta_model.pkl",
                 use_synergy: bool = False,
                 synergy_cols: list = None,
                 random_state: int = 42):
        """
        :param mode: "hard_voting", "soft_voting", or "stacking"
        :param save_path: path to save or load the meta-model
        :param use_synergy: if True, synergy columns remain in X or we do synergy weighting
        :param synergy_cols: list of columns that store synergy info
        :param random_state: for reproducibility in base or final classifier
        """
        self.mode = mode
        self.save_path = save_path
        self.model = None
        self.fitted = False
        self.use_synergy = use_synergy
        self.synergy_cols = synergy_cols if synergy_cols else []
        self.random_state = random_state
        # If synergy weighting is desired, you can handle that in train() or predict().

    def build(self, base_models: Dict[str, object]):
        """
        Build the meta-model ensemble from a dict of base models:
            base_models = {
                "dt": DecisionTreeClassifier(...),
                "svc": SVC(...),
                "lr": LogisticRegression(...)
            }

        We store them as estimators. 
        Then we create a VotingClassifier or StackingClassifier depending on self.mode.
        For stacking, we'll use a logistic regression as final_estimator by default.
        """
        estimators = [(name, model) for name, model in base_models.items()]

        if self.mode == "hard_voting":
            self.model = VotingClassifier(
                estimators=estimators, 
                voting="hard"
            )
        elif self.mode == "soft_voting":
            self.model = VotingClassifier(
                estimators=estimators,
                voting="soft"
            )
        elif self.mode == "stacking":
            # Use a logistic regression meta-model by default
            final_estimator = LogisticRegression(random_state=self.random_state, max_iter=500)
            self.model = StackingClassifier(
                estimators=estimators,
                final_estimator=final_estimator,
                passthrough=False  # if True, pass original features along with base predictions
            )
        else:
            raise ValueError("Invalid meta-model mode. Choose 'hard_voting','soft_voting','stacking'.")

    def train(self,
              X: pd.DataFrame,
              y: pd.Series,
              do_cross_val: bool = False,
              cv_folds: int = 5):
        """
        Train the meta-model. Optionally do cross-validation for reporting.

        If synergy usage is advanced (like weighting samples by synergy), 
        you can incorporate that logic here. E.g. pass sample_weight to model.fit() 
        if synergy is used as weight. For demonstration, we skip it.

        :param X: feature DataFrame (include synergy columns if needed)
        :param y: target
        :param do_cross_val: if True, run cross_val_score for a quick estimate
        :param cv_folds: number of folds in cross-validation
        """
        if self.model is None:
            raise RuntimeError("Meta-model has not been built. Call .build(base_models) first.")

        # Optional synergy weighting approach:
        # if self.use_synergy and self.synergy_cols:
        #     sample_weight = X[self.synergy_cols].mean(axis=1).clip(lower=0.1) # just an example
        # else:
        #     sample_weight = None

        # We must handle synergy columns if they exist. If synergy is not used for classification directly,
        # we might drop them from X or keep them. We'll keep them by default if synergy is a real feature.
        # Fit the model
        self.model.fit(X, y)  # e.g. add sample_weight=sample_weight if your logic requires it
        self.fitted = True

        if do_cross_val:
            scores = cross_val_score(self.model, X, y, cv=cv_folds, scoring="accuracy")
            print(f"[MetaModel] Cross-validation (cv={cv_folds}) accuracy mean: {scores.mean():.4f}")

        # Save
        self._save_model()

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Generate predictions using the meta-model. If not loaded or fitted, attempts to load.
        :param X: Feature DataFrame
        :return: array of predicted labels
        """
        if not self.fitted or self.model is None:
            # Attempt to load
            self._load_model()
            if not self.fitted or self.model is None:
                raise RuntimeError("Meta-model is not trained or cannot be loaded.")
        return self.model.predict(X)

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        If the meta-model supports predict_proba (like soft voting or stacking),
        returns probability estimates.
        """
        if not self.fitted or self.model is None:
            self._load_model()
            if not self.fitted or self.model is None:
                raise RuntimeError("Meta-model is not trained or cannot be loaded.")

        if hasattr(self.model, "predict_proba"):
            return self.model.predict_proba(X)
        else:
            raise AttributeError(f"Model type '{self.mode}' does not support predict_proba.")

    def evaluate(self, X: pd.DataFrame, y: pd.Series) -> float:
        """
        Evaluate the meta-model's accuracy. 
        Print a classification report as well for more detail.

        :param X: features
        :param y: true target
        :return: float accuracy
        """
        preds = self.predict(X)
        acc = accuracy_score(y, preds)
        print(f"Meta-model accuracy: {acc:.4f}")
        print("Classification Report:")
        print(classification_report(y, preds))
        return acc

    def _save_model(self):
        """
        Save the meta-model to disk using joblib.
        """
        os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
        dump(self.model, self.save_path)
        print(f"[MetaModel] Model saved to {self.save_path}")

    def _load_model(self):
        """
        Load the meta-model from disk if present.
        """
        if os.path.exists(self.save_path):
            self.model = load(self.save_path)
            self.fitted = True
            print(f"[MetaModel] Model loaded from {self.save_path}")
        else:
            print(f"[MetaModel] No saved model found at {self.save_path}")


if __name__ == "__main__":
    # Example usage
    from sklearn.datasets import make_classification
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.svm import SVC
    from sklearn.linear_model import LogisticRegression

    # Generate some dummy classification data
    X_data, y_data = make_classification(n_samples=300, n_features=10, random_state=42)
    X_data = pd.DataFrame(X_data, columns=[f"feat_{i}" for i in range(10)])
    y_data = pd.Series(y_data)

    # Define base models
    base_models_dict = {
        "dt": DecisionTreeClassifier(random_state=42),
        "svc": SVC(probability=True, random_state=42),
        "lr": LogisticRegression(random_state=42, max_iter=300)
    }

    # Build and train a stacking meta-model
    meta = MetaModel(mode="stacking", save_path="meta_model_stack.pkl", use_synergy=False)
    meta.build(base_models_dict)
    meta.train(X_data, y_data, do_cross_val=True, cv_folds=3)

    # Evaluate on the same data (for demonstration only)
    acc = meta.evaluate(X_data, y_data)
    print(f"Final accuracy on same data: {acc:.4f}")

    # We can also do meta.predict_proba if we want
    if meta.mode in ["soft_voting", "stacking"]:
        proba = meta.predict_proba(X_data)
        print("Probability example:", proba[:5])

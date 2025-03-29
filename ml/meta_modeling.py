#!/usr/bin/env python3
import pandas as pd
import numpy as np
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from joblib import dump, load

class MetaModel:
    """
    Meta-model that combines predictions from multiple base models using ensemble methods.
    Supports training, saving, loading, and inference.
    """
    def __init__(self, mode="hard_voting", save_path="ml/models/meta_model.pkl"):
        """
        Initializes the meta-model.
        
        Parameters:
          mode: "hard_voting", "soft_voting", or "stacking"
          save_path: Path to save the trained meta-model.
        """
        self.mode = mode
        self.save_path = save_path
        self.model = None

    def build(self, base_models: dict):
        """
        Build the meta-model ensemble.
        
        Parameters:
          base_models: A dictionary of {model_name: sklearn-compatible model}
        """
        estimators = [(name, model) for name, model in base_models.items()]
        if self.mode == "hard_voting":
            self.model = VotingClassifier(estimators=estimators, voting="hard")
        elif self.mode == "soft_voting":
            self.model = VotingClassifier(estimators=estimators, voting="soft")
        elif self.mode == "stacking":
            # Placeholder: replace with sklearn's StackingClassifier if stacking is needed.
            self.model = VotingClassifier(estimators=estimators, voting="soft")
        else:
            raise ValueError("Invalid meta-model mode. Choose 'hard_voting', 'soft_voting', or 'stacking'.")

    def train(self, X: pd.DataFrame, y: pd.Series):
        """
        Train the meta-model using the provided features and target.
        
        Parameters:
          X: Feature DataFrame.
          y: Target Series.
        """
        if self.model is None:
            raise RuntimeError("Meta-model has not been built. Call .build(base_models) first.")
        self.model.fit(X, y)
        dump(self.model, self.save_path)
        print(f"Meta-model trained and saved to {self.save_path}")

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Generate predictions using the meta-model.
        
        Parameters:
          X: Feature DataFrame.
          
        Returns:
          Predictions as a numpy array.
        """
        if self.model is None:
            try:
                self.model = load(self.save_path)
                print("Meta-model loaded from disk.")
            except Exception as e:
                raise RuntimeError("Meta-model is not trained or cannot be loaded.") from e
        return self.model.predict(X)

    def evaluate(self, X: pd.DataFrame, y_true: pd.Series) -> float:
        """
        Evaluate the meta-model's accuracy.
        
        Parameters:
          X: Feature DataFrame.
          y_true: True target values.
          
        Returns:
          Accuracy score.
        """
        y_pred = self.predict(X)
        accuracy = accuracy_score(y_true, y_pred)
        print(f"Meta-model accuracy: {accuracy:.4f}")
        return accuracy

if __name__ == "__main__":
    # Example usage:
    from sklearn.datasets import make_classification
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.svm import SVC

    # Generate dummy classification data
    X, y = make_classification(n_samples=200, n_features=10, random_state=42)
    X = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(10)])
    y = pd.Series(y)

    # Define base models
    base_models = {
        "dt": DecisionTreeClassifier(random_state=42),
        "svc": SVC(probability=True, random_state=42),
        "lr": LogisticRegression(random_state=42, max_iter=200)
    }

    # Build and train the meta-model
    meta = MetaModel(mode="hard_voting", save_path="meta_model.pkl")
    meta.build(base_models)
    meta.train(X, y)
    
    # Evaluate the meta-model
    meta.evaluate(X, y)

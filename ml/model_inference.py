# ml/model_inference.py

import pandas as pd
import joblib
from typing import List, Union

def load_model(model_path: str):
    """
    Loads a saved model from disk.
    """
    return joblib.load(model_path)


def score_signals(
    df: pd.DataFrame,
    features: List[str],
    model_path: str,
    score_column: str = "ml_score"
) -> pd.DataFrame:
    """
    Uses a trained model to score signals (predict probability of success).

    Parameters:
    - df: DataFrame with features
    - features: List of feature column names
    - model_path: Path to trained model
    - score_column: Name of column to store prediction scores

    Returns:
    - df with added score column
    """
    df = df.copy()
    model = load_model(model_path)

    # Only score valid rows
    valid_df = df.dropna(subset=features)
    scores = model.predict_proba(valid_df[features])[:, 1]  # prob of class=1

    # Inject scores back into full df
    df.loc[valid_df.index, score_column] = scores
    return df

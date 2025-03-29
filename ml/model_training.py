# ml/model_training.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
import joblib
import os

def train_model(
    df: pd.DataFrame,
    features: list[str],
    model_type: str = "xgboost",
    model_path: str = "ml/models/model.pkl"
):
    """
    Trains a supervised ML model on labeled signal data.
    
    Parameters:
    - df: dataframe with features + label
    - features: columns to use as input
    - model_type: "xgboost" or "random_forest"
    - model_path: path to save the trained model
    """
    df = df.dropna(subset=features + ["label"])
    X = df[features]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    if model_type == "xgboost":
        model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            use_label_encoder=False,
            eval_metric="logloss"
        )
    elif model_type == "random_forest":
        model = RandomForestClassifier(n_estimators=100, max_depth=5)
    else:
        raise ValueError("Unsupported model type")

    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)

    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)

    print(f"✅ Model trained and saved to: {model_path}")
    print(f"🔍 Validation Accuracy: {score:.4f}")
    return model

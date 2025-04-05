#!/usr/bin/env python3
"""
model_training.py

Provides functions to:
1. Generate training features from price data + optional signal data.
2. Train a classification (or regression) model.
3. Optionally perform hyperparameter optimization (grid or random search).
4. Save the trained model to disk.

Example usage (classification):
    from model_training import generate_features, train_model
    price_data = ...
    signals = ...
    features_df = generate_features(price_data, signals)
    model = train_model(features_df, model_type="rf", do_hyperparam_search=False)
    # Then joblib.dump(model, "trained_model.pkl") or something similar
"""

import pandas as pd
import numpy as np
from typing import Optional, Union, Dict
import joblib

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, classification_report, mean_squared_error
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

###########################
# 1) Feature Generation
###########################

# def generate_features(price_data: pd.DataFrame,
#                       signal_data: pd.DataFrame = None,
#                       synergy_map: dict = None,
#                       label_col: str = "target",
#                       dropna: bool = True) -> pd.DataFrame:
#     """
#     Generate features from price data and optional signals. 
#     This replicates or extends your logic with:
#       - Merging price_data with signal_data using an asof or normal merge
#       - Building synergy score if synergy_map is provided
#       - Possibly adding user-defined label if it already exists in price_data 
#         or if you want to do a separate label generation pipeline

#     :param price_data: DataFrame with columns used as features (like rsi, momentum, etc.)
#     :param signal_data: optional DataFrame with columns like demark_signal, pivot_signal
#     :param synergy_map: optional dict e.g. {"demark_signal":1.0, "pivot_signal":1.5} to build synergy_score
#     :param label_col: if your data already has a 'target' or label column. If not found, no label is included
#     :param dropna: if True, drop rows with any NaN. If you prefer partial cleaning, adjust logic
#     :return: DataFrame with features + optional label column
#     """
#     df_feat = price_data.copy()

#     # Merge signals if provided
#     if signal_data is not None and not signal_data.empty:
#         df_feat = pd.merge_asof(
#             df_feat.sort_values("datetime"),
#             signal_data.sort_values("datetime"),
#             on="datetime",
#             direction="backward"
#         )

#     # synergy_map => sum weighted columns
#     if synergy_map is not None:
#         synergy_score = np.zeros(len(df_feat))
#         for col, weight in synergy_map.items():
#             if col in df_feat.columns:
#                 synergy_score += df_feat[col].astype(float) * weight
#         df_feat["synergy_score"] = synergy_score

#     # If we want to ensure we have the label column. Some pipelines might do a separate label gen step.
#     # We'll keep label if it exists
#     if label_col not in df_feat.columns:
#         print(f"[generate_features] Warning: '{label_col}' not found in DataFrame columns.")
#     else:
#         print(f"[generate_features] Found label column '{label_col}' in data.")

#     # Drop NaN
#     if dropna:
#         df_feat = df_feat.dropna().reset_index(drop=True)

#     return df_feat
def generate_features(price_df: pd.DataFrame, signal_df: pd.DataFrame = None, synergy_map: dict = None) -> pd.DataFrame:

    df = price_df.copy()

    # Basic features
    # Correct RSI calculation
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))

    df['sma'] = df['close'].rolling(window=20).mean()
    df['momentum'] = df['close'] - df['close'].shift(5)

    # Add signals if provided
    if signal_df is not None and 'datetime' in signal_df.columns:
        df = df.merge(signal_df, on='datetime', how='left')
        if 'signal' in df.columns:
            df['signal_binary'] = df['signal'].map({'buy': 1, 'sell': 0}).fillna(0)


    # Target label — future price up/down
    if 'close' in df.columns:
        df['future_close'] = df['close'].shift(-5)
        df['target'] = (df['future_close'] > df['close']).astype(int)
        df.drop(columns=['future_close'], inplace=True)
        df.dropna(subset=['target'], inplace=True)


    # Synergy score from weighted signal columns (if synergy_map is provided)
    if signal_df is not None and synergy_map is not None:
        synergy_score = np.zeros(len(df))
        for col, weight in synergy_map.items():
            if col in df.columns:
                synergy_score += df[col].astype(float) * weight
            else:
                print(f"[generate_features] Warning: column '{col}' not found in signals for synergy.")
        df["synergy_score"] = synergy_score


    # Drop rows with any NaNs — can be changed to more selective cleaning if needed
    df = df.dropna().reset_index(drop=True)

    # Confirm 'target' exists after generation
    if "target" not in df.columns:
        raise ValueError("[generate_features] 'target' column was not generated.")


    return df




###########################
# 2) Model Training
###########################

def train_model(features_df: pd.DataFrame,
                model_type: str = "rf",
                label_col: str = "target",
                do_hyperparam_search: bool = False,
                param_grid: dict = None,
                task: str = "classification",
                random_state: int = 42):
    """
    Train a model (classification or regression) on the given features.

    :param features_df: DataFrame containing features + label column
    :param model_type: "rf" => random forest, "lr" => logistic regression, or "rfr" => random forest regressor
    :param label_col: the name of the label column
    :param do_hyperparam_search: if True, run a GridSearchCV using param_grid
    :param param_grid: a dict of hyperparameters for the selected model
    :param task: "classification" or "regression"
    :param random_state: for reproducibility
    :return: trained model
    """
    # 1) Separate X,y
    if label_col not in features_df.columns:
        raise ValueError(f"[train_model] Label column '{label_col}' not found in features DataFrame.")

    X = features_df.drop(columns=[label_col])
    X = X.select_dtypes(include=[np.number])  # Only keep numeric features
    y = features_df[label_col]


    # 2) Model selection
    if task == "classification":
        if model_type == "rf":
            model = RandomForestClassifier(random_state=random_state)
        elif model_type == "lr":
            model = LogisticRegression(random_state=random_state, max_iter=500)
        else:
            raise ValueError(f"Unsupported classification model_type: {model_type}")
    elif task == "regression":
        if model_type == "rf" or model_type == "rfr":
            model = RandomForestRegressor(random_state=random_state)
        else:
            raise ValueError(f"Unsupported regression model_type: {model_type}")
    else:
        raise ValueError(f"Unsupported task type: {task}. Use 'classification' or 'regression'.")

    # 3) Optionally do param search
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=random_state)
    # 4) Train/test split and training

    if do_hyperparam_search:
        search = GridSearchCV(model, param_grid, cv=3,
                          scoring="accuracy" if task == "classification" else "neg_mean_squared_error")
        search.fit(X_train, y_train)
        model = search.best_estimator_
        print(f"[train_model] Best params from search: {search.best_params_}")
    else:
        model.fit(X_train, y_train)


    return model


def save_trained_model(model, model_path: str = "trained_model.pkl"):
    """
    Saves the trained model to disk using joblib.
    """
    joblib.dump(model, model_path)
    print(f"[save_trained_model] Model saved to {model_path}")


###########################
# Example usage
###########################
if __name__ == "__main__":
    from datetime import datetime, timedelta
    np.random.seed(42)

    # Create dummy data
    # Suppose we have a classification scenario
    # with some features e.g. 'rsi','mom','synergy_score'
    # plus 'target' as label
    n = 200
    df_example = pd.DataFrame({
        "datetime": pd.date_range("2022-01-01", periods=n, freq="D"),
        "rsi": np.random.randint(10, 90, size=n),
        "mom": np.random.randn(n),
        "some_signal": np.random.randint(0,2,size=n),
        "target": np.random.randint(0,2,size=n)
    })

    # We might want synergy_map that sums synergy from 'some_signal' with weight=1.5
    synergy_map = {
        "some_signal": 1.5
    }

    # Generate features
    feat_df = generate_features(df_example, signal_data=None, synergy_map=synergy_map, label_col="target")

    # Train a random forest classification
    model = train_model(
        features_df=feat_df,
        model_type="rf",
        label_col="target",
        do_hyperparam_search=False,
        task="classification"
    )

    # Save model
    save_trained_model(model, "trained_model.pkl")

#!/usr/bin/env python3
"""
model_inference.py

Provides functions to load a trained model and perform inference (prediction)
on new/unseen data, possibly incorporating synergy, advanced signals, or 
precomputed technical indicators.

Typical usage:
  model = load_trained_model("trained_model.pkl")
  inference_df = build_inference_features(price_data, signals)
  predictions_df = predict_with_model(model, inference_df, task="classification")

Steps:
  1) load_trained_model(model_path)
  2) build_inference_features(...) => prepare the same feature set used in training
  3) predict_with_model(model, features_df, task="classification" or "regression")
"""

import pandas as pd
import numpy as np
import joblib
from typing import Union

########################
# 1) Load the trained model
########################

def load_trained_model(model_path: str):
    """
    Load a trained model (e.g. sklearn pipeline or estimator) from disk using joblib.
    """
    try:
        model = joblib.load(model_path)
        print(f"[ModelInference] Model loaded from {model_path}")
        return model
    except Exception as e:
        raise RuntimeError(f"[ModelInference] Error loading model from {model_path}: {e}") from e

########################
# 2) Build inference features
########################

def build_inference_features(price_data: pd.DataFrame,
                             signal_data: pd.DataFrame = None,
                             synergy_map: dict = None) -> pd.DataFrame:
    """
    Construct a feature DataFrame for inference, ensuring it matches
    the structure used during training.

    Steps:
      - Merge or asof-merge price_data with signal_data
      - If synergy_map is provided, build synergy_score
      - Possibly compute or recompute TAs if needed
      - Return final DataFrame of features (no label column, obviously)

    :param price_data: DataFrame of price data with TAs or columns used in training
    :param signal_data: optional DataFrame of signals. 
                       If needed, do an asof merge or standard merge. 
    :param synergy_map: optional dict => { 'demark_signal':1.0, 'pivot_signal':1.5 }, etc. 
                       If synergy_map is None, skip synergy creation
    :return: DataFrame with final features
    """
    # 1) Start with price_data
    df_features = price_data.copy()

    # 2) If signal_data is provided, let's do an asof merge to align
    #    or a normal merge if that suits your data. We'll do asof for demonstration:
    if signal_data is not None and not signal_data.empty:
        df_features = pd.merge_asof(
            df_features.sort_values("datetime"), 
            signal_data.sort_values("datetime"),
            on="datetime",
            direction="backward"
        )
    else:
        # If we need placeholders
        pass

    # 3) synergy creation if synergy_map is given
    if synergy_map is not None:
        synergy_cols = [col for col in synergy_map.keys() if col in df_features.columns]
        synergy_scores = np.zeros(len(df_features))
        for col in synergy_cols:
            weight = synergy_map[col]
            synergy_scores += df_features[col].astype(float) * weight
        df_features["synergy_score"] = synergy_scores
    else:
        # if synergy is used in the model but no synergy map is given, you might set synergy=0
        pass

    # If we know exactly which columns are needed for the model,
    # we might subset or reorder them. For demonstration, we skip that step.
    # In a real pipeline, we might do:
    # required_cols = ["rsi","mom","macd", "demark_signal","synergy_score",...]
    # df_features = df_features[required_cols].copy()

    # drop any rows missing essential columns
    df_features = df_features.dropna().reset_index(drop=True)
    return df_features

########################
# 3) Predict with model
########################

def predict_with_model(model,
                       features_df: pd.DataFrame,
                       task: str = "classification") -> pd.DataFrame:
    """
    Generate predictions using the loaded model. 
    For classification, returns predicted labels and optionally probabilities if model supports them.
    For regression, returns predicted numeric values.

    :param model: the loaded/trained estimator
    :param features_df: DataFrame with columns that match the training
    :param task: "classification" or "regression"
    :return: The features_df with extra columns e.g. 'prediction' and (if classification & supports) 'pred_proba'
    """
    # We'll do a copy so we can add columns
    df_pred = features_df.copy()

    # Predict
    y_pred = model.predict(df_pred)
    df_pred['prediction'] = y_pred

    if task == "classification":
        # If the model supports predict_proba, add that:
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(df_pred)
            # If binary, shape is Nx2. If multi-class, NxN
            # We'll store them in columns like 'prob_class_0', 'prob_class_1' ...
            n_classes = probs.shape[1]
            for c in range(n_classes):
                df_pred[f'prob_class_{c}'] = probs[:, c]
        else:
            # No prob method
            pass

    elif task == "regression":
        # already have y_pred, do nothing else
        pass
    else:
        raise ValueError(f"Unsupported task type: {task}")

    return df_pred

########################
# Example main
########################

if __name__ == "__main__":
    from datetime import datetime, timedelta
    import numpy as np
    # Suppose we have a pipeline that already created a "trained_model.pkl"

    # 1) Load the model
    model_path = "trained_model.pkl"
    try:
        model = load_trained_model(model_path)
    except RuntimeError as e:
        print(e)
        model = None

    if model is not None:
        # 2) Build inference data
        # Let's create dummy price_data
        dates = pd.date_range("2023-01-01", periods=15, freq='D')
        close_prices = 100 + np.cumsum(np.random.randn(15))
        price_df = pd.DataFrame({
            'datetime': dates,
            'close': close_prices,
            'rsi': np.random.randint(20, 80, size=15),
            'demark_signal': np.random.randint(0,2,size=15),
        })
        # dummy signals
        signals_df = pd.DataFrame({
            'datetime': dates[::3],
            'pivot_signal': np.random.randint(0,2,size=len(dates[::3]))
        })

        synergy_map = {
            "demark_signal": 1.0,
            "pivot_signal": 1.5
        }
        # create feature DataFrame
        feat_df = build_inference_features(price_df, signals_df, synergy_map=synergy_map)

        # 3) Predict with the model
        # Suppose it's a classification model
        predictions_df = predict_with_model(model, feat_df, task="classification")
        print("Inference sample:\n", predictions_df.head(10))

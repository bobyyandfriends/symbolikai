#!/usr/bin/env python3
import pandas as pd
import joblib
from ml.model_training import generate_features

def load_trained_model(model_path: str):
    """
    Load a trained model from disk using joblib.
    """
    return joblib.load(model_path)

def predict_with_model(model, price_data: pd.DataFrame, signals: pd.DataFrame) -> pd.DataFrame:
    """
    Generate predictions using the trained model.
    
    This function:
      - Generates features from price_data and signals.
      - Uses the model to predict the target.
      - Returns the features DataFrame with an added 'prediction' column.
    """
    features_df = generate_features(price_data, signals)
    X = features_df.drop(columns=['target'])
    predictions = model.predict(X)
    features_df['prediction'] = predictions
    return features_df

if __name__ == "__main__":
    # Example usage:
    import numpy as np
    from datetime import datetime, timedelta

    # Create dummy price data with precomputed indicators
    dates = pd.date_range(start="2022-01-01", periods=200, freq='D')
    prices = np.cumsum(np.random.randn(200)) + 100
    price_data = pd.DataFrame({
        'datetime': dates,
        'close': prices
    })
    # Dummy RSI and SMA for demonstration
    price_data['rsi'] = 50 + 10 * np.sin(np.linspace(0, 10, 200))
    price_data['sma'] = price_data['close'].rolling(window=10, min_periods=10).mean()
    price_data = price_data.dropna().reset_index(drop=True)
    
    # Create dummy signals data
    signals = pd.DataFrame({
        'datetime': dates[10:],
        'signal': np.random.choice(['buy', 'sell'], size=len(dates[10:]))
    })
    
    # Load the trained model (make sure "trained_model.pkl" exists from model_training.py)
    model_path = "trained_model.pkl"
    try:
        model = load_trained_model(model_path)
    except Exception as e:
        print(f"Error loading model from {model_path}: {e}")
        model = None
    
    if model is not None:
        predictions_df = predict_with_model(model, price_data, signals)
        print("Predictions Sample:")
        print(predictions_df.head())

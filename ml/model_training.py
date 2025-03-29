#!/usr/bin/env python3
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

def generate_features(price_data: pd.DataFrame, signals: pd.DataFrame) -> pd.DataFrame:
    """
    Generate features from price and signal data.
    
    For demonstration purposes, this function computes:
      - RSI (assumed precomputed in price_data)
      - SMA (assumed precomputed in price_data)
      - Momentum (difference between current close and previous close)
      - A binary feature from the signal column (buy=1, sell=0)
      
    Additionally, the target variable is defined as whether the next day's close is higher than the current day's close.
    
    Assumptions:
      - price_data has columns: 'datetime', 'close', 'rsi', 'sma'
      - signals has columns: 'datetime' and 'signal'
    
    Returns a DataFrame with features and a target column.
    """
    df = price_data.copy().sort_values('datetime').reset_index(drop=True)
    
    # Calculate momentum as difference between current and previous close
    df['momentum'] = df['close'].diff()
    
    # Merge signals with price data using nearest previous datetime match
    features = pd.merge_asof(df, signals.sort_values('datetime'), on='datetime', direction='backward')
    
    # Create a binary feature for signal type: buy=1, sell=0, other=0
    features['signal_binary'] = features['signal'].apply(lambda x: 1 if isinstance(x, str) and 'buy' in x.lower() else 0)
    
    # Define target: 1 if next day's close is higher than current close, else 0.
    features['target'] = (features['close'].shift(-1) > features['close']).astype(int)
    
    # Drop rows with missing values (first row for momentum, last row for target)
    features = features.dropna().reset_index(drop=True)
    
    # Select the feature columns plus the target
    feature_cols = ['rsi', 'sma', 'momentum', 'signal_binary', 'target']
    return features[feature_cols]

def train_model(features_df: pd.DataFrame):
    """
    Train a RandomForestClassifier model to predict the 'target' using generated features.
    
    Splits the data into training and test sets, trains the model, evaluates its performance,
    and returns the trained model.
    """
    X = features_df.drop(columns=['target'])
    y = features_df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    y_pred = clf.predict(X_test)
    print("Model Accuracy:", accuracy_score(y_test, y_pred))
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    
    return clf

if __name__ == "__main__":
    # Example usage with dummy data
    from datetime import datetime, timedelta
    np.random.seed(42)
    
    # Create dummy price data with precomputed indicators
    dates = pd.date_range(start="2022-01-01", periods=200, freq='D')
    prices = np.cumsum(np.random.randn(200)) + 100
    price_data = pd.DataFrame({
        'datetime': dates,
        'close': prices
    })
    # For demonstration, create dummy RSI and SMA values
    price_data['rsi'] = 50 + 10 * np.sin(np.linspace(0, 10, 200))
    price_data['sma'] = price_data['close'].rolling(window=10, min_periods=10).mean()
    price_data = price_data.dropna().reset_index(drop=True)
    
    # Create dummy signals data
    signals = pd.DataFrame({
        'datetime': dates[10:],
        'signal': np.random.choice(['buy', 'sell'], size=len(dates[10:]))
    })
    
    # Generate features and target variable
    features_df = generate_features(price_data, signals)
    print("Generated Features Sample:")
    print(features_df.head())
    
    # Train the model and evaluate its performance
    model = train_model(features_df)
    
    # Save the trained model to disk
    joblib.dump(model, "trained_model.pkl")
    print("Model saved as 'trained_model.pkl'")

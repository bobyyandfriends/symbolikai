#!/usr/bin/env python3
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

class EnvironmentClassifier:
    """
    Classifies market environments using unsupervised learning (KMeans).
    This classifier can tag each bar or period as belonging to a regime (e.g., trending, choppy).
    """
    def __init__(self, n_clusters=3, random_state=42):
        self.n_clusters = n_clusters
        self.scaler = StandardScaler()
        self.model = KMeans(n_clusters=n_clusters, random_state=random_state)
        self.fitted = False

    def extract_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract regime classification features from raw price data.
        Features include:
          - return: percentage change in close prices
          - volatility: rolling standard deviation of returns over 10 periods
          - momentum: difference between the current close and its 10-period rolling mean
          - range: difference between high and low for the bar
        Returns a DataFrame with these features, dropping rows with missing values.
        """
        df_feat = df.copy()
        df_feat["return"] = df_feat["close"].pct_change()
        df_feat["volatility"] = df_feat["return"].rolling(10).std()
        df_feat["momentum"] = df_feat["close"] - df_feat["close"].rolling(10).mean()
        df_feat["range"] = df_feat["high"] - df_feat["low"]
        return df_feat[["return", "volatility", "momentum", "range"]].dropna()

    def fit(self, df: pd.DataFrame) -> None:
        """
        Fit the environment classifier on the provided price DataFrame.
        Extracts features, scales them, and fits the KMeans model.
        """
        features = self.extract_features(df)
        scaled_features = self.scaler.fit_transform(features)
        self.model.fit(scaled_features)
        self.fitted = True

    def predict(self, df: pd.DataFrame) -> pd.Series:
        """
        Predict environment labels (e.g., 0, 1, 2) for each row in the price DataFrame.
        Raises an error if the model has not been fitted.
        """
        if not self.fitted:
            raise RuntimeError("Model not trained. Call .fit(df) first.")
        features = self.extract_features(df)
        scaled = self.scaler.transform(features)
        preds = self.model.predict(scaled)
        result = pd.Series(preds, index=features.index, name="environment")
        return result

    def fit_predict(self, df: pd.DataFrame) -> pd.Series:
        """
        Fit the model and then predict environment labels in one step.
        """
        self.fit(df)
        return self.predict(df)

if __name__ == "__main__":
    # Example usage:
    import numpy as np
    from datetime import datetime, timedelta
    
    # Create dummy price data for demonstration
    dates = pd.date_range(start="2022-01-01", periods=50, freq='D')
    np.random.seed(42)
    prices = np.cumsum(np.random.randn(50)) + 100
    price_data = pd.DataFrame({
        'datetime': dates,
        'open': prices + np.random.randn(50) * 0.5,
        'high': prices + np.random.rand(50),
        'low': prices - np.random.rand(50),
        'close': prices,
        'volume': np.random.randint(100, 1000, size=50)
    })
    
    # Instantiate and fit the environment classifier
    classifier = EnvironmentClassifier(n_clusters=3)
    classifier.fit(price_data)
    
    # Predict environment labels and display a sample
    env_labels = classifier.predict(price_data)
    print("Environment labels:")
    print(env_labels.head())

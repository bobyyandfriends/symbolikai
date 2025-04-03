#!/usr/bin/env python3
"""
environment_classifier.py

Classifies market environments (e.g., trending, mean-reverting, high-vol, etc.)
using unsupervised learning (KMeans or optional GMM). Supports synergy or pivot
features if present in the data. Returns environment labels for each time row.

Example usage in SymbolikAI:
  env_clf = EnvironmentClassifier(n_clusters=3)
  features_df = env_clf.extract_features(price_data, synergy_df, pivot_df)
  env_clf.fit(features_df)
  labels = env_clf.predict(features_df)
  # Now you have an environment label for each row, e.g. 0, 1, or 2

Then in strategies or backtester, you might filter or adapt logic by environment.
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler


class EnvironmentClassifier:
    """
    Classifies market environments using unsupervised learning. By default, KMeans.
    Optionally supports a GMM approach if desired.

    Steps:
      1. extract_features(): from raw data (price_data, synergy, pivot, etc.)
      2. fit(features_df): train the clustering model
      3. predict(features_df): get environment labels
      4. (optional) transform(...) or label distribution analysis

    Features to consider:
      - returns or volatility
      - synergy_score or pivot alignment
      - Hurst exponent or other fractal measure
      - volume changes
      - fundamental or macro data
    """

    def __init__(self,
                 n_clusters=3,
                 method='kmeans',
                 random_state=42):
        """
        :param n_clusters: Number of clusters (typical 3-5)
        :param method: 'kmeans' or 'gmm'
        :param random_state: for reproducibility
        """
        self.n_clusters = n_clusters
        self.method = method
        self.random_state = random_state

        self.scaler = StandardScaler()
        self.model = None
        self.fitted = False

    def extract_features(self,
                         df_price: pd.DataFrame,
                         df_synergy: pd.DataFrame = None,
                         df_pivot: pd.DataFrame = None) -> pd.DataFrame:
        """
        Extract regime classification features from raw data. 
        Adjust as needed to your final synergy/pivot usage.

        :param df_price: DataFrame containing OHLCV or at least 'close'
                         can use columns like 'close', 'volume'
                         must be time-indexed or have a 'datetime' col
        :param df_synergy: optional synergy signals
        :param df_pivot: optional pivot or fractal signals
        :return: DataFrame with extracted columns, ready for fit/predict
        """
        # We'll do a simple approach:
        #   1) daily returns
        #   2) rolling volatility
        #   3) synergy_score if present
        #   4) pivot_signal or pivot_count if present

        df_feat = pd.DataFrame()

        # ensure sorting by time or something
        df_price = df_price.sort_index() if df_price.index.is_monotonic else df_price.sort_values('datetime')
        df_feat['returns'] = df_price['close'].pct_change().fillna(0.0)

        # rolling volatility (14-day for example)
        window_vol = 14
        df_feat['volatility'] = df_feat['returns'].rolling(window_vol).std().fillna(method='bfill')

        # synergy
        if df_synergy is not None and 'synergy_score' in df_synergy.columns:
            # merge on date if needed
            # or if df_synergy has same index, we can just join
            # let's assume same index for simplicity:
            df_feat['synergy'] = df_synergy['synergy_score'].fillna(0.0)
        else:
            df_feat['synergy'] = 0.0

        # pivot
        if df_pivot is not None and 'pivot_signal' in df_pivot.columns:
            # e.g. pivot_signal is 1 or 0
            df_feat['pivot_signal'] = df_pivot['pivot_signal'].fillna(0.0)
        else:
            df_feat['pivot_signal'] = 0.0

        # drop NaNs from rolling
        df_feat = df_feat.dropna()

        return df_feat

    def fit(self, features: pd.DataFrame):
        """
        Fit the clustering model on the provided features DataFrame.
        We standardize the features first, then cluster.
        """
        # standardize
        X = self.scaler.fit_transform(features.values)
        if self.method == 'kmeans':
            self.model = KMeans(n_clusters=self.n_clusters,
                                random_state=self.random_state)
        elif self.method == 'gmm':
            self.model = GaussianMixture(n_components=self.n_clusters,
                                         random_state=self.random_state)
        else:
            raise ValueError(f"Unknown method: {self.method}")

        self.model.fit(X)
        self.fitted = True

    def predict(self, features: pd.DataFrame) -> pd.Series:
        """
        Predict environment labels for each row in features.
        Returns a pd.Series of cluster IDs or environment labels.

        NOTE: must call fit(...) first
        """
        if not self.fitted or self.model is None:
            raise RuntimeError("EnvironmentClassifier not fitted yet.")

        X = self.scaler.transform(features.values)

        if self.method == 'kmeans':
            labels = self.model.predict(X)
        else:  # GMM
            labels = self.model.predict(X)

        return pd.Series(labels, index=features.index, name='environment_label')

    def get_cluster_centers(self):
        """
        If KMeans, return cluster centers in unscaled space for interpretability.
        If GMM, returns means of each cluster. 
        Must handle both differently.
        """
        if not self.fitted or self.model is None:
            return None

        if self.method == 'kmeans':
            # unscale centers
            scaled_centers = self.model.cluster_centers_
            unscaled = self.scaler.inverse_transform(scaled_centers)
            return unscaled
        elif self.method == 'gmm':
            scaled_means = self.model.means_
            unscaled = self.scaler.inverse_transform(scaled_means)
            return unscaled
        else:
            return None

    def transform(self, features: pd.DataFrame) -> np.ndarray:
        """
        If you want the cluster distance or posterior probabilities
        For KMeans: transform returns distances to cluster centers
        For GMM:    predict_proba returns cluster membership probabilities

        :param features:
        :return: array of shape (n_samples, n_clusters)
        """
        if not self.fitted or self.model is None:
            raise RuntimeError("EnvironmentClassifier not fitted yet.")

        X = self.scaler.transform(features.values)

        if self.method == 'kmeans':
            # distances to each cluster center
            dist = self.model.transform(X)
            return dist
        else:
            # GMM probabilities
            probs = self.model.predict_proba(X)
            return probs


if __name__ == "__main__":
    # Example usage:
    # Let's create dummy price data
    idx = pd.date_range(start="2023-01-01", periods=30, freq="D")
    prices = np.cumsum(np.random.randn(30)) + 100
    df_price = pd.DataFrame({'close': prices}, index=idx)

    # synergy or pivot (dummy)
    synergy = pd.DataFrame({'synergy_score': np.random.rand(30)}, index=idx)
    pivot = pd.DataFrame({'pivot_signal': np.random.randint(0,2,size=30)}, index=idx)

    # init classifier
    env_clf = EnvironmentClassifier(n_clusters=3, method='kmeans')
    feats = env_clf.extract_features(df_price, synergy, pivot)
    env_clf.fit(feats)
    labels = env_clf.predict(feats)
    print("Environment labels:\n", labels.value_counts())

    # see cluster centers
    centers = env_clf.get_cluster_centers()
    if centers is not None:
        print("\nUnscaled cluster centers:\n", centers)

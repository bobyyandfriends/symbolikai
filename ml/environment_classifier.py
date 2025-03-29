# ml/environment_classifier.py

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

class EnvironmentClassifier:
    """
    Classifies market environments using unsupervised learning (KMeans).
    Can be used to tag each bar or period as belonging to a regime (e.g., trending, choppy).
    """

    def __init__(self, n_clusters=3, random_state=42):
        self.n_clusters = n_clusters
        self.scaler = StandardScaler()
        self.model = KMeans(n_clusters=n_clusters, random_state=random_state)
        self.fitted = False

    def extract_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extracts regime classification features from raw price data.
        These can include volatility, momentum, returns, etc.
        """
        df_feat = df.copy()

        df_feat["return"] = df_feat["close"].pct_change()
        df_feat["volatility"] = df_feat["return"].rolling(10).std()
        df_feat["momentum"] = df_feat["close"] - df_feat["close"].rolling(10).mean()
        df_feat["range"] = df_feat["high"] - df_feat["low"]

        return df_feat[["return", "volatility", "momentum", "range"]].dropna()

    def fit(self, df: pd.DataFrame) -> None:
        """
        Fits the environment classifier on a price DataFrame.
        """
        features = self.extract_features(df)
        scaled_features = self.scaler.fit_transform(features)
        self.model.fit(scaled_features)
        self.fitted = True

    def predict(self, df: pd.DataFrame) -> pd.Series:
        """
        Returns a Series of environment labels (e.g., 0, 1, 2) for each row.
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
        Combines fit and predict into one step.
        """
        self.fit(df)
        return self.predict(df)


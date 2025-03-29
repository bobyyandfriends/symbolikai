#!/usr/bin/env python3
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import pandas_ta as ta

# Import functions from our ML module
from ml.model_training import generate_features, train_model
import joblib

def main():
    st.title("Model Trainer")
    st.write("Upload historical price data (CSV) to train an ML model.")
    
    price_file = st.file_uploader("Upload Price Data (CSV)", type=["csv"])
    
    if price_file is not None:
        try:
            # Expect a CSV with at least a 'datetime' and 'close' column
            price_data = pd.read_csv(price_file, parse_dates=["datetime"])
            st.success("Price data loaded successfully.")
            st.write("Price Data Preview:")
            st.dataframe(price_data.head())
        except Exception as e:
            st.error(f"Error loading price data: {e}")
            return
    else:
        st.info("Please upload price data to proceed.")
        return

    # Sidebar for training parameters
    st.sidebar.header("Training Parameters")
    future_window = st.sidebar.slider("Future window (bars)", 5, 20, 10)
    profit_threshold = st.sidebar.number_input("Profit threshold (%)", min_value=0.0, value=3.0, step=0.1) / 100.0
    loss_threshold = st.sidebar.number_input("Loss threshold (%)", min_value=-10.0, value=-2.0, step=0.1) / 100.0

    # Check if essential technical indicators are present; if not, compute them
    if "rsi" not in price_data.columns or "sma" not in price_data.columns:
        st.info("Computing default technical indicators (RSI and SMA) for feature generation...")
        price_data["rsi"] = ta.rsi(price_data["close"], length=14)
        price_data["sma"] = price_data["close"].rolling(window=10, min_periods=10).mean()
        price_data = price_data.dropna().reset_index(drop=True)
    
    # Create a dummy signals DataFrame for feature generation (for simplicity, mark all rows as 'buy')
    signals = pd.DataFrame({
        "datetime": price_data["datetime"],
        "signal": ["buy"] * len(price_data)
    })
    
    if st.button("Train Model"):
        st.subheader("Generating Features")
        # Generate features and target using our ML module
        features_df = generate_features(price_data, signals)
        st.write("Sample of Generated Features:")
        st.dataframe(features_df.head())
        
        st.info("Training model, please wait...")
        # Train the model (RandomForestClassifier in our example)
        model = train_model(features_df)
        
        st.success("Model trained successfully!")
        
        # Display sample predictions
        X_sample = features_df.drop(columns=["target"])
        predictions = model.predict(X_sample)
        features_df["prediction"] = predictions
        st.write("Sample Predictions:")
        st.dataframe(features_df.head())
        
        st.info("Trained model saved as 'trained_model.pkl'.")

if __name__ == "__main__":
    main()

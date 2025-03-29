# ui/pages/model_trainer.py

import streamlit as st
from ml.model_training import train_model_for_strategy
from ml.model_inference import evaluate_model_performance
import joblib
import os

MODEL_DIR = "models"

def display():
    st.title("🤖 Train Strategy Models")

    strategy_name = st.selectbox("Select Strategy to Train", ["Perfection9Up", "Combo_C13_P9", "S13Variant"])
    model_type = st.selectbox("Model Type", ["xgboost", "random_forest", "lightgbm"])

    if st.button("Train Model"):
        st.write(f"Training model for `{strategy_name}` using `{model_type}`...")
        model, metrics, commentary = train_model_for_strategy(strategy_name, model_type)

        st.success("✅ Training Complete")
        st.write("📈 Evaluation Metrics:")
        st.json(metrics)

        st.write("🧠 Model Commentary:")
        st.text(commentary)

        # Save model
        if not os.path.exists(MODEL_DIR):
            os.makedirs(MODEL_DIR)
        model_path = os.path.join(MODEL_DIR, f"{strategy_name}_{model_type}.pkl")
        joblib.dump(model, model_path)
        st.info(f"Model saved to `{model_path}`")

    st.markdown("---")

    if st.checkbox("Evaluate Existing Model"):
        strategy_name = st.text_input("Strategy Name", "Perfection9Up")
        model_type = st.text_input("Model Type", "xgboost")

        model_path = os.path.join(MODEL_DIR, f"{strategy_name}_{model_type}.pkl")
        if os.path.exists(model_path):
            st.success(f"Found saved model at `{model_path}`")
            model = joblib.load(model_path)
            eval_metrics, notes = evaluate_model_performance(model)
            st.write("📊 Evaluation Results:")
            st.json(eval_metrics)
            st.write("🔎 Observations:")
            st.text(notes)
        else:
            st.error("Model not found.")


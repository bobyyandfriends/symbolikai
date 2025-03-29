# ui/app.py

import streamlit as st
from ui.pages import strategy_tester, signal_explorer, model_trainer, comparison_dashboard

st.set_page_config(page_title="SymbolikAI", layout="wide")

# Sidebar Navigation
st.sidebar.title("SymbolikAI Control Panel")
page = st.sidebar.radio("Navigate to:", [
    "Strategy Tester",
    "Signal Explorer",
    "Model Trainer",
    "Strategy Comparison"
])

# Page Routing
if page == "Strategy Tester":
    strategy_tester.run()
elif page == "Signal Explorer":
    signal_explorer.run()
elif page == "Model Trainer":
    model_trainer.run()
elif page == "Strategy Comparison":
    comparison_dashboard.run()

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("Created with ❤️ for internal trading research.")

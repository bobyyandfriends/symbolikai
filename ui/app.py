#!/usr/bin/env python3
import streamlit as st
from ui.pages.strategy_tester import strategy_tester_page
from ui.pages.signal_explorer import main as signal_explorer_page
from ui.pages.model_trainer import main as model_trainer_page
from ui.pages.comparison_dashboard import comparison_dashboard_page

def main():
    st.sidebar.title("Navigation")
    selected_page = st.sidebar.radio("Go to", 
                                     ["Strategy Tester", "Signal Explorer", "Model Trainer", "Comparison Dashboard"])
    
    if selected_page == "Strategy Tester":
        strategy_tester_page()
    elif selected_page == "Signal Explorer":
        signal_explorer_page()
    elif selected_page == "Model Trainer":
        model_trainer_page()
    elif selected_page == "Comparison Dashboard":
        comparison_dashboard_page()
    else:
        st.write("Page not found.")

if __name__ == "__main__":
    main()

#-- Imports --
import streamlit as st
import pandas as pd
import numpy as np
from strategies.sma_crossover import SMACrossover
import vectorbt as vbt

def Header():
    # --- Header & Controls ---
    st.title("Quant Startegy Tester")

    # Control Bar (Top Section)
    col1, col2, col3, col4 = st.columns([2, 2, 1, 1])

    with col1:
        
        strategy = st.selectbox(
            "Strategy",
            ["SMA", "EMA", "MACD", "RSI", "Bollinger"],
            index=0
        )
        st.session_state.strategy = strategy

    with col2:
        if "Timeframe" not in st.session_state:
            st.session_state.timeframe = "All Time"
        timeframe = st.select_slider(
            "Timeframe",
            ["1D", "1W", "1mo", "3mo", "6mo", "1Y", "5Y", "YTD", "All Time"],
            value=st.session_state.timeframe,

        )
        st.session_state.timeframe = timeframe

    with col3:
        st.write("") # Spacer
        st.write("") # Spacer
        if st.button("Run", type="secondary", use_container_width=True):
            if st.session_state.strategy == "SMA":
                df = []
                if st.session_state.timeframe == "All Time":
                    df = vbt.YFData.download("BTC-USD").get("Close")
                else:
                    df = vbt.YFData.download("BTC-USD", period="" + st.session_state.timeframe).get("Close")


                st.session_state.portfolio = SMACrossover(df, sma_fast=20, sma_slow=50)


        

    with col4:
        st.write("") # Spacer
        st.write("") # Spacer
        st.button("Export", type="primary", use_container_width=True)

    st.markdown("---")

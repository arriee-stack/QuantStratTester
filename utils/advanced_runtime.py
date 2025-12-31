from utils.run_strategy import runStrategy
import vectorbt as vbt
from strategies.sma_crossover import SMACrossover
import streamlit as st


def advancedRuntimeSMA(tickers, fast, slow, equitiesArray):
    for i in tickers:
        df = vbt.YFData.download(i).get("Close")
        equitiesArray.append(
            runStrategy(
                SMACrossover(df, sma_fast=fast, sma_slow=slow)
            ).equityCurveData()
        )

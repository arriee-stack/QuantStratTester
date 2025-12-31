# -- Imports --
import streamlit as st
from top_nav import Header
from utils.run_strategy import runStrategy
import altair as alt
import vectorbt as vbt
import pandas as pd
from strategies.sma_crossover import SMACrossover

# -- Page Config --

tickerSuggestions = [
    "BTC-USD",
    "ETH-USD",
    "SOL-USD",
    "DOGE-USD",
    "LUNA-USD",
    "UNI-USD",
    "AAVE-USD",
    "LINK-USD",
    "XRP-USD",
]


st.set_page_config(
    page_title="QuantStratTester",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="expanded",
)
st.markdown(
    """
<style>
/* Targets the main block container to set a custom max-width */
section[data-testid="stMain"] > div[data-testid="stMainBlockContainer"] {
    max-width: 80rem; /* Example: set to 80rem */
    padding-left: 1rem;
    padding-right: 1rem;
}
</style>
""",
    unsafe_allow_html=True,
)

Header()
tab1, tab2, tab3 = st.tabs(["Trades", "Equity", "Deep Analysis"])
if "portfolio" not in st.session_state:
    st.session_state["portfolio"] = None


with tab1:
    if st.session_state.portfolio != None:
        graphBox = st.container(border=True)
        runStrat = runStrategy(st.session_state.portfolio)
        graphBox.plotly_chart(runStrat.tradesChart(), use_container_width=True)
        # st.line_chart(runStrat.tradesChart())
        # print(runStrat.tradesChart())
with tab2:
    if st.session_state.portfolio != None:
        runStrat = runStrategy(st.session_state.portfolio)
        df = runStrat.equityCurveData()
        if st.session_state.timeframe == "All Time":
            df2 = vbt.Portfolio.from_holding(
                vbt.YFData.download("BTC-USD").get("Close"),
                init_cash=100,
            ).value()
        else:
            df2 = vbt.Portfolio.from_holding(
                vbt.YFData.download("BTC-USD", period=st.session_state.timeframe).get(
                    "Close"
                ),
                init_cash=100,
            ).value()
        df2 = df2.reset_index()
        df2.columns = ["date", "equity"]
        df["benchmark"] = df2["equity"]

        df_long = df.melt(
            id_vars="time",
            value_vars=["equity", "benchmark"],
            var_name="series",
            value_name="value",
        )
        area1 = (
            alt.Chart(df)
            .mark_area(color="#4C78A8", opacity=0.05, line={"color": "#4C78A8"})
            .encode(
                x="time:T",
                y="equity:Q",
            )
        )

        area2 = (
            alt.Chart(df)
            .mark_area(color="#F58518", opacity=0.05, line={"color": "#F58518"})
            .encode(
                x="time:T",
                y="benchmark:Q",
            )
        )

        area = area1 + area2
        st.altair_chart(area, use_container_width=True)
with tab3:
    if st.session_state.portfolio != None:
        options = st.multiselect(
            "Tickers",
            tickerSuggestions,
            default=["BTC-USD"],
        )
        if st.session_state.strategy == "SMA":
            smaSlow = st.slider("Slow SMA", 0, 200, 50)
            smaFast = st.slider("Fast SMA", 0, 200, 20)
            portfolioEquities = []
            for i in options:

                runStrat = runStrategy(st.session_state.portfolio)
                df = vbt.YFData.download(i).get("Close")
                portfolioEquities.append(
                    runStrategy(
                        SMACrossover(df, sma_fast=smaFast, sma_slow=smaSlow)
                    ).equityCurveData()
                )

        deepAnalysisGraphBox = st.container(border=True)

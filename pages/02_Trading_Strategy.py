import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import joblib
import polars as pl
from src.styles import apply_custom_style

st.set_page_config(page_title="Trading Strategy", layout="wide")
apply_custom_style()

st.title("Algorithmic Trading Strategy")
st.markdown("Performance evaluation of the model-driven execution engine.")

# Load data for backtesting (using local processed data for speed)
try:
    df_all = pl.read_parquet("data/processed/features.parquet")
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META"]
    
    selected_ticker = st.sidebar.selectbox("Select Asset for Backtest", tickers)
    
    # Filter and prep
    df = df_all.filter(pl.col("Ticker") == selected_ticker).sort("Date").tail(250)
    
    # 1. Run Strategy Simulation
    clf = joblib.load("models/classifier.joblib")
    features = joblib.load("models/features_list.joblib")
    
    X = df.select(features).to_pandas().values
    probs = clf.predict_proba(X)[:, 1]
    
    # Strategy Logic: Buy if prob > 0.55, Sell if < 0.45
    # For backtesting, we use the next day's real return
    returns = (np.exp(df["Target_Log_Return"].to_numpy()) - 1)
    
    signals = []
    for p in probs:
        if p > 0.55: signals.append(1) # Buy
        elif p < 0.45: signals.append(-1) # Sell
        else: signals.append(0) # Neutral
    
    # Calculate Strategy Returns
    strategy_returns = np.array(signals) * returns
    
    # 2. Cumulative Equity
    initial_investment = 10000
    equity_curve = initial_investment * (1 + strategy_returns).cumprod()
    benchmark_curve = initial_investment * (1 + returns).cumprod()
    
    # 3. Metrics
    total_return = (equity_curve[-1] / initial_investment - 1) * 100
    win_rate = (strategy_returns > 0).sum() / (np.array(signals) != 0).sum() * 100
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""<div class="kpi-container"><div class="kpi-label">Strategy Return</div><div class="kpi-value">{total_return:.1f}%</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="kpi-container"><div class="kpi-label">Win Rate</div><div class="kpi-value">{win_rate:.1f}%</div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="kpi-container"><div class="kpi-label">Benchmark Return</div><div class="kpi-value">{((benchmark_curve[-1]/initial_investment)-1)*100:.1f}%</div></div>""", unsafe_allow_html=True)

    # 4. Equity Curve Visual
    st.subheader("Equity Curve Simulation")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Date"].to_list(), y=equity_curve, name="AI Strategy", line=dict(color='#1D1917', width=3)))
    fig.add_trace(go.Scatter(x=df["Date"].to_list(), y=benchmark_curve, name="Buy & Hold", line=dict(color='#EAE2D6', width=2)))
    
    fig.update_layout(
        template="plotly_white",
        yaxis_title="Portfolio Value ($)",
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.info("Note: Backtest simulates execution at the closing price of each day based on the model's signal for the following session.")

except Exception as e:
    st.error(f"Error loading backtest data: {e}")

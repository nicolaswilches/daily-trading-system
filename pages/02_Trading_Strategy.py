import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import joblib
import polars as pl
from src.styles import apply_custom_style, MOCHA, get_plotly_template

apply_custom_style()

st.title("Algorithmic Trading Strategy")
st.markdown("Performance evaluation of the model-driven execution engine.")

# ── Sidebar Controls ──────────────────────────────────────────────────
tickers = ["AAPL", "MSFT", "AMZN", "TSLA", "NVDA"]
selected_ticker = st.sidebar.radio("Select Asset for Backtest", tickers)

st.sidebar.divider()
st.sidebar.markdown("**Backtest Parameters**")
lookback = st.sidebar.slider("Lookback (trading days)", 60, 500, 250, step=10)
initial_investment = st.sidebar.number_input(
    "Initial Capital ($)",
    min_value=1000,
    max_value=1_000_000,
    value=10_000,
    step=1000,
)
buy_threshold = st.sidebar.slider("Buy threshold", 0.50, 0.70, 0.55, step=0.01)
sell_threshold = st.sidebar.slider("Sell threshold", 0.30, 0.50, 0.45, step=0.01)

try:
    with st.spinner("Running backtest..."):
        df_all = pl.read_parquet("data/processed/features.parquet")
        df = (
            df_all.filter(pl.col("Ticker") == selected_ticker)
            .sort("Date")
            .tail(lookback)
        )

        clf = joblib.load("models/classifier.joblib")
        features = joblib.load("models/features_list.joblib")

        X = df.select(features).to_pandas().values
        probs = clf.predict_proba(X)[:, 1]

        returns = np.exp(df["Target_Log_Return"].to_numpy()) - 1

        signals = []
        for p in probs:
            if p > buy_threshold:
                signals.append(1)
            elif p < sell_threshold:
                signals.append(-1)
            else:
                signals.append(0)
        signals = np.array(signals)

        strategy_returns = signals * returns
        equity_curve = initial_investment * (1 + strategy_returns).cumprod()
        benchmark_curve = initial_investment * (1 + returns).cumprod()

        # ── Metrics ───────────────────────────────────────────
        total_return = (equity_curve[-1] / initial_investment - 1) * 100
        active_trades = signals != 0
        win_rate = (
            (strategy_returns[active_trades] > 0).sum() / active_trades.sum() * 100
            if active_trades.sum() > 0
            else 0
        )
        bench_return = (benchmark_curve[-1] / initial_investment - 1) * 100
        num_trades = int(active_trades.sum())

        # Max drawdown
        running_max = np.maximum.accumulate(equity_curve)
        drawdown = (equity_curve - running_max) / running_max
        max_dd = drawdown.min() * 100

        k1, k2, k3, k4, k5 = st.columns(5)
        for col, label, value in [
            (k1, "Strategy Return", f"{total_return:.1f}%"),
            (k2, "Win Rate", f"{win_rate:.1f}%"),
            (k3, "Benchmark Return", f"{bench_return:.1f}%"),
            (k4, "Max Drawdown", f"{max_dd:.1f}%"),
            (k5, "Total Trades", str(num_trades)),
        ]:
            with col:
                st.markdown(
                    f'<div class="kpi-container"><div class="kpi-label">{label}</div>'
                    f'<div class="kpi-value">{value}</div></div>',
                    unsafe_allow_html=True,
                )

        # ── Equity Curve ──────────────────────────────────────
        st.markdown("#### Equity Curve")
        layout = get_plotly_template()
        dates = df["Date"].to_list()

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=dates,
                y=equity_curve,
                name="AI Strategy",
                line=dict(color=MOCHA["blue"], width=2.5),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=dates,
                y=benchmark_curve,
                name="Buy & Hold",
                line=dict(color=MOCHA["overlay1"], width=1.5, dash="dot"),
            )
        )
        fig.update_layout(
            layout,
            height=440,
            yaxis_title="Portfolio Value ($)",
            hovermode="x unified",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="left",
                x=0,
            ),
        )
        st.plotly_chart(fig, use_container_width=True)

        # ── Drawdown Chart ────────────────────────────────────
        with st.expander("Drawdown"):
            fig_dd = go.Figure()
            fig_dd.add_trace(
                go.Scatter(
                    x=dates,
                    y=drawdown * 100,
                    fill="tozeroy",
                    line=dict(color=MOCHA["red"], width=1),
                    fillcolor=f"rgba(243, 139, 168, 0.2)",
                    name="Drawdown %",
                )
            )
            fig_dd.update_layout(
                layout,
                height=250,
                yaxis_title="Drawdown %",
                hovermode="x unified",
                showlegend=False,
            )
            st.plotly_chart(fig_dd, use_container_width=True)

        # ── Trade Log ─────────────────────────────────────────
        with st.expander("Trade Log"):
            log_dates = df["Date"].to_list()
            close_prices = df["Close"].to_list()
            log_data = []
            for i, (s, r) in enumerate(zip(signals, strategy_returns)):
                if s != 0:
                    action = "BUY" if s == 1 else "SELL"
                    log_data.append(
                        {
                            "Date": log_dates[i],
                            "Action": action,
                            "Price": f"${close_prices[i]:.2f}",
                            "Return": f"{r * 100:+.2f}%",
                            "Prob Up": f"{probs[i] * 100:.1f}%",
                        }
                    )
            if log_data:
                trade_df = pd.DataFrame(log_data).sort_values("Date", ascending=False)
                st.dataframe(trade_df, use_container_width=True, hide_index=True)
            else:
                st.info("No trades executed with the current thresholds.")

        st.info(
            "Backtest simulates execution at the closing price of each day "
            "based on the model's signal for the following session."
        )

except Exception as e:
    st.error(f"Error loading backtest data: {e}")

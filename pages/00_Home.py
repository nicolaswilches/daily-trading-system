import streamlit as st
from src.styles import apply_custom_style, MOCHA

apply_custom_style()

# ── Hero ──────────────────────────────────────────────────────────────
st.title("Automated Daily Trading System")
st.markdown(
    "A quantitative platform that forecasts short-term equity movements "
    "using machine-learning models trained on historical price action and "
    "corporate fundamentals."
)

st.divider()

# ── Core Functionalities ─────────────────────────────────────────────
st.markdown("#### What This System Does")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        f"""
        <div class="feature-card">
            <h4>Predictive Analysis</h4>
            <p>
                LightGBM classification and regression models, tuned with
                Bayesian optimisation, predict whether a stock's price will
                rise and estimate the expected magnitude of the move.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        f"""
        <div class="feature-card">
            <h4>Real-Time Market Data</h4>
            <p>
                Live price feeds from the SimFin API are processed through
                the same feature-engineering pipeline used during training,
                delivering up-to-date trading signals on demand.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        f"""
        <div class="feature-card">
            <h4>Backtesting Engine</h4>
            <p>
                A historical simulation evaluates the strategy against a
                buy-and-hold benchmark, reporting return, win rate,
                drawdown, and a full equity curve.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("")

# ── Objectives ────────────────────────────────────────────────────────
col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown("#### System Objectives")
    st.markdown(
        f"""
        The platform operates on a **dual-objective** framework designed
        for institutional-grade decision making:

        1. **Predictive Accuracy** — Utilise gradient-boosted models optimised
           for precision to identify high-probability directional moves.
        2. **Real-Time Integration** — Seamless connection to external market
           data so that every prediction is based on the latest available
           information.
        3. **Algorithmic Strategy** — Convert statistical probabilities into
           concrete execution signals (BUY / HOLD / SELL) with clearly defined
           confidence thresholds.

        The classification model determines the likelihood of a positive price
        move in the next trading session, while a companion regression model
        forecasts the expected log-return magnitude.
        """
    )

with col_right:
    st.markdown("#### Development Team")
    st.markdown(
        f"""
        <div class="kpi-container">
            <div class="kpi-label">Lead Data Scientist</div>
            <div style="font-size: 1.15rem; font-weight: 600; color: {MOCHA["text"]}; margin-bottom: 12px;">
                Nicolas Wilches
            </div>
            <hr style="border: 0; border-top: 1px solid {MOCHA["surface2"]}; margin: 14px 0;">
            <div class="kpi-label">System Status</div>
            <div style="color: {MOCHA["green"]}; font-weight: 600; font-size: 0.95rem;">
                Production Ready
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### Supported Assets")
    tickers = ["AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "NVDA", "META"]
    chips_html = "".join(f'<span class="ticker-chip">{t}</span>' for t in tickers)
    st.markdown(chips_html, unsafe_allow_html=True)

st.divider()
st.markdown(
    "Navigate to **Market Analysis** in the sidebar to begin real-time forecasting."
)

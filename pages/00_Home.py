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

# ── Core Functionalities ─────────────────────────────────────────────
st.markdown('<div class="home-section">', unsafe_allow_html=True)
st.markdown("#### What This System Does")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        """
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
        """
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
        """
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
st.markdown("</div>", unsafe_allow_html=True)

# ── System Objectives ─────────────────────────────────────────────────
st.markdown('<div class="home-section">', unsafe_allow_html=True)
st.markdown("#### System Objectives")

obj1, obj2, obj3 = st.columns(3)

with obj1:
    st.markdown(
        """
        <div class="objective-card">
            <h5>Predictive Accuracy</h5>
            <p>
                Utilise gradient-boosted models optimised for precision 
                to identify high-probability directional moves with 
                statistical confidence thresholds.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with obj2:
    st.markdown(
        """
        <div class="objective-card">
            <h5>Real-Time Integration</h5>
            <p>
                Seamless connection to external market data ensures 
                every prediction is based on the latest available 
                information and market conditions.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with obj3:
    st.markdown(
        """
        <div class="objective-card">
            <h5>Algorithmic Strategy</h5>
            <p>
                Convert statistical probabilities into concrete execution 
                signals (BUY / HOLD / SELL) with clearly defined 
                confidence thresholds.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
st.markdown("</div>", unsafe_allow_html=True)

# ── Development Team ──────────────────────────────────────────────────
st.markdown('<div class="home-section">', unsafe_allow_html=True)
st.markdown("#### Development Team — 8 Labs")
st.markdown(
    f'<p style="color: {MOCHA["subtext1"]}; font-size: 0.95rem; margin-bottom: 1.5rem;">Meet the team:</p>',
    unsafe_allow_html=True,
)

# Professional initial-based avatars with distinct colors
team_members = [
    ("Nicolas Wilches", "Lead Data Scientist", "#007AFF"),
    ("Madelyn Ehni", "Data Engineer", "#34C759"),
    ("Salah Mneimne", "ML Engineer", "#FF9500"),
    ("Gilles Hamers", "Quantitative Analyst", "#AF52DE"),
    ("Alberto Cabezudo", "Software Engineer", "#FF2D92"),
]

team_cols = st.columns(5)

for col, (name, role, color) in zip(team_cols, team_members):
    with col:
        initials = "".join([n[0] for n in name.split()]).upper()
        st.markdown(
            f"""
            <div class="team-card">
                <div class="team-avatar" style="background-color: {color}; display: flex; align-items: center; justify-content: center;">
                    <span style="color: white; font-weight: 600; font-size: 1.2rem; font-family: 'Inter', sans-serif;">{initials}</span>
                </div>
                <div class="member-name">{name}</div>
                <div class="member-role">{role}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
st.markdown("</div>", unsafe_allow_html=True)

# ── Supported Assets ──────────────────────────────────────────────────
st.markdown('<div class="home-section">', unsafe_allow_html=True)
st.markdown("#### Supported Assets")

# Removed GOOG and META as requested
tickers = ["AAPL", "MSFT", "AMZN", "TSLA", "NVDA"]
chips_html = "".join(f'<span class="ticker-chip">{t}</span>' for t in tickers)
st.markdown(chips_html, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    f"""
    <div style="text-align: center; margin-top: 2rem; padding: 20px; 
                background-color: {MOCHA["surface0"]}; border-radius: 8px;
                border-left: 4px solid {MOCHA["green"]};">
        <p style="color: {MOCHA["text"]}; font-weight: 600; margin: 0;">
            Navigate to <strong>Go Live</strong> in the sidebar to begin real-time forecasting
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

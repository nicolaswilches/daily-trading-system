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

features = [
    ("📊", "Predictive Analysis", "#007AFF", "LightGBM classification and regression models, tuned with Bayesian optimisation, predict whether a stock's price will rise and estimate the expected magnitude of the move."),
    ("⚡", "Real-Time Market Data", "#34C759", "Live price feeds from the SimFin API are processed through the same feature-engineering pipeline used during training, delivering up-to-date trading signals on demand."),
    ("🔁", "Backtesting Engine", "#FF9500", "A historical simulation evaluates the strategy against a buy-and-hold benchmark, reporting return, win rate, drawdown, and a full equity curve."),
]

for col, (icon, title, color, text) in zip([c1, c2, c3], features):
    with col:
        st.markdown(
            f"""
            <div class="feature-card" style="border-top: 3px solid {color};">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <h4 style="color: {color}; margin: 0;">{title}</h4>
                    <div style="font-size: 2rem;">{icon}</div>
                </div>
                <p>{text}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
st.markdown("</div>", unsafe_allow_html=True)

# ── System Objectives ─────────────────────────────────────────────────
st.markdown('<div class="home-section">', unsafe_allow_html=True)
st.markdown("#### System Objectives")

obj1, obj2, obj3 = st.columns(3)

objectives = [
    ("🎯", "Predictive Accuracy", "#AF52DE", "Utilise gradient-boosted models optimised for precision to identify high-probability directional moves with statistical confidence thresholds."),
    ("🔗", "Real-Time Integration", "#FF2D92", "Seamless connection to external market data ensures every prediction is based on the latest available information and market conditions."),
    ("🔀", "Algorithmic Strategy", "#FF9500", "Convert statistical probabilities into concrete execution signals (BUY / HOLD / SELL) with clearly defined confidence thresholds."),
]

for col, (icon, title, color, text) in zip([obj1, obj2, obj3], objectives):
    with col:
        st.markdown(
            f"""
            <div class="objective-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <h5 style="color: {color}; margin: 0;">{title}</h5>
                    <div style="font-size: 2rem;">{icon}</div>
                </div>
                <p>{text}</p>
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
    ("Nicolas Wilches", "Lead Data Scientist", "#007AFF", "https://linkedin.com/in/nicolaswilches"),
    ("Madelyn Ehni", "Data Engineer", "#34C759", "https://linkedin.com/in/madelyn-ehni"),
    ("Salah Mneimne", "ML Engineer", "#FF9500", "https://linkedin.com/in/salahmneimne"),
    ("Gilles Hamers", "Quantitative Analyst", "#AF52DE", "https://linkedin.com/in/gillesham"),
    ("Alberto Cabezudo", "Software Engineer", "#FF2D92", "https://linkedin.com/in/albertocabezudo"),
]

team_cols = st.columns(5)

for col, (name, role, color, linkedin) in zip(team_cols, team_members):
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
                <a href="{linkedin}" target="_blank" style="text-decoration: none;">
                    <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" 
                         width="20" style="margin-top: 8px; opacity: 0.8;"/>
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )
st.markdown("</div>", unsafe_allow_html=True)

# ── Supported Assets ──────────────────────────────────────────────────
st.markdown('<div class="home-section">', unsafe_allow_html=True)
st.markdown("#### Supported Assets")

tickers = ["AAPL", "MSFT", "AMZN", "TSLA", "NVDA"]

cols = st.columns(len(tickers))
for col, ticker in zip(cols, tickers):
    with col:
        st.markdown(
            f"""
            <div style="display: flex; flex-direction: column; align-items: center; gap: 8px;">
                <img src="https://assets.parqet.com/logos/symbol/{ticker}?format=png" 
                     width="50" height="50" 
                     style="border-radius: 12px; object-fit: contain;"/>
                <span class="ticker-chip">{ticker}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

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

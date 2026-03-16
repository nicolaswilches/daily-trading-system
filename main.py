import streamlit as st

# ── Entry Point ───────────────────────────────────────────────────────
# Streamlit's multi-page app uses the pages/ directory automatically.
# This file sets global config and redirects to the Home page.

st.set_page_config(
    page_title="Daily Trading System",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Redirect to Home — the actual content lives in pages/00_Home.py.
# When users navigate to the root, they see the Home page content.
pg = st.navigation(
    [
        st.Page("pages/00_Home.py", title="Home", default=True),
        st.Page("pages/01_Market_Analysis.py", title="Go Live"),
        st.Page("pages/02_Trading_Strategy.py", title="Trading Strategy"),
        st.Page("pages/03_Methodology.py", title="Methodology"),
    ]
)
pg.run()

import streamlit as st
import plotly.graph_objects as go
import plotly.io as pio

# ── Catppuccin Mocha Palette ─────────────────────────────────────────
MOCHA = {
    "rosewater": "#f5e0dc",
    "flamingo": "#f2cdcd",
    "pink": "#f5c2e7",
    "mauve": "#cba6f7",
    "red": "#f38ba8",
    "maroon": "#eba0ac",
    "peach": "#fab387",
    "yellow": "#f9e2af",
    "green": "#a6e3a1",
    "teal": "#94e2d5",
    "sky": "#89dceb",
    "sapphire": "#74c7ec",
    "blue": "#89b4fa",
    "lavender": "#b4befe",
    "text": "#cdd6f4",
    "subtext1": "#bac2de",
    "subtext0": "#a6adc8",
    "overlay2": "#9399b2",
    "overlay1": "#7f849c",
    "overlay0": "#6c7086",
    "surface2": "#585b70",
    "surface1": "#45475a",
    "surface0": "#313244",
    "base": "#1e1e2e",
    "mantle": "#181825",
    "crust": "#11111b",
}


def get_plotly_template():
    """Return a Plotly layout template themed with Catppuccin Mocha."""
    return go.Layout(
        paper_bgcolor=MOCHA["base"],
        plot_bgcolor=MOCHA["base"],
        font=dict(family="Inter, sans-serif", color=MOCHA["text"], size=13),
        xaxis=dict(
            gridcolor=MOCHA["surface1"],
            zerolinecolor=MOCHA["surface1"],
            linecolor=MOCHA["surface1"],
            tickfont=dict(color=MOCHA["subtext0"]),
        ),
        yaxis=dict(
            gridcolor=MOCHA["surface1"],
            zerolinecolor=MOCHA["surface1"],
            linecolor=MOCHA["surface1"],
            tickfont=dict(color=MOCHA["subtext0"]),
        ),
        legend=dict(
            font=dict(color=MOCHA["subtext1"]),
            bgcolor="rgba(0,0,0,0)",
        ),
        hoverlabel=dict(
            bgcolor=MOCHA["surface0"],
            font_color=MOCHA["text"],
            bordercolor=MOCHA["surface2"],
        ),
        margin=dict(l=0, r=0, t=0, b=0),
    )


def apply_custom_style():
    """Inject custom CSS for the Catppuccin Mocha theme."""
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

        /* ── Base ─────────────────────────────────────────────── */
        .stApp {{
            background-color: {MOCHA["base"]};
            color: {MOCHA["text"]};
            font-family: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif;
        }}

        /* ── Typography ───────────────────────────────────────── */
        h1, h2, h3 {{
            color: {MOCHA["text"]};
            font-weight: 600;
            letter-spacing: -0.02em;
        }}
        h1 {{ font-size: 1.75rem; }}

        p, li, span, label, .stMarkdown {{
            color: {MOCHA["subtext1"]};
        }}

        /* ── KPI Cards ────────────────────────────────────────── */
        .kpi-container {{
            background-color: {MOCHA["surface0"]};
            border: 1px solid {MOCHA["surface2"]};
            border-radius: 10px;
            padding: 20px 24px;
            margin-bottom: 16px;
        }}

        .kpi-label {{
            font-size: 0.75rem;
            color: {MOCHA["overlay1"]};
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 6px;
            font-weight: 500;
        }}

        .kpi-value {{
            font-size: 1.6rem;
            font-weight: 600;
            color: {MOCHA["text"]};
            line-height: 1.2;
        }}

        .kpi-delta {{
            font-size: 0.85rem;
            margin-top: 4px;
            font-weight: 500;
        }}

        /* ── Feature Cards (Home Page) ────────────────────────── */
        .feature-card {{
            background-color: {MOCHA["surface0"]};
            border: 1px solid {MOCHA["surface2"]};
            border-radius: 10px;
            padding: 28px 24px;
            height: 100%;
        }}

        .feature-card h4 {{
            color: {MOCHA["text"]};
            font-size: 1rem;
            margin-bottom: 8px;
        }}

        .feature-card p {{
            color: {MOCHA["subtext0"]};
            font-size: 0.85rem;
            line-height: 1.5;
        }}

        /* ── Signal Banner ────────────────────────────────────── */
        .signal-banner {{
            border-radius: 10px;
            padding: 20px 24px;
            margin: 8px 0 16px 0;
        }}

        .signal-banner h2 {{
            margin: 0 0 4px 0;
            font-size: 1.5rem;
        }}

        .signal-banner .conf {{
            font-size: 0.85rem;
            font-weight: 400;
        }}

        /* ── Sidebar ──────────────────────────────────────────── */
        [data-testid="stSidebar"] {{
            background-color: {MOCHA["mantle"]};
            border-right: 1px solid {MOCHA["surface0"]};
        }}

        [data-testid="stSidebar"] * {{
            color: {MOCHA["subtext1"]};
        }}

        /* ── Tabs ─────────────────────────────────────────────── */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 0;
            border-bottom: 1px solid {MOCHA["surface1"]};
        }}

        .stTabs [data-baseweb="tab"] {{
            background-color: transparent;
            color: {MOCHA["overlay1"]};
            border-bottom: 2px solid transparent;
            padding: 8px 20px;
            font-weight: 500;
        }}

        .stTabs [aria-selected="true"] {{
            color: {MOCHA["text"]};
            border-bottom: 2px solid {MOCHA["blue"]};
            background-color: transparent;
        }}

        /* ── Buttons ──────────────────────────────────────────── */
        .stButton > button {{
            background-color: {MOCHA["blue"]};
            color: {MOCHA["base"]};
            border-radius: 6px;
            border: none;
            padding: 0.45rem 1rem;
            font-weight: 500;
        }}

        .stButton > button:hover {{
            background-color: {MOCHA["sapphire"]};
        }}

        /* ── Selectbox & Inputs ───────────────────────────────── */
        .stSelectbox > div > div {{
            background-color: {MOCHA["surface0"]};
            border-color: {MOCHA["surface2"]};
            color: {MOCHA["text"]};
        }}

        /* ── Expanders ────────────────────────────────────────── */
        .streamlit-expanderHeader {{
            background-color: {MOCHA["surface0"]};
            color: {MOCHA["subtext1"]};
            border-radius: 8px;
        }}

        /* ── Dividers ─────────────────────────────────────────── */
        hr {{
            border-color: {MOCHA["surface1"]};
        }}

        /* ── DataFrames ───────────────────────────────────────── */
        .stDataFrame {{
            border: 1px solid {MOCHA["surface1"]};
            border-radius: 8px;
        }}

        /* ── Info / Warning boxes ─────────────────────────────── */
        .stAlert {{
            background-color: {MOCHA["surface0"]};
            border: 1px solid {MOCHA["surface2"]};
            color: {MOCHA["subtext1"]};
            border-radius: 8px;
        }}

        /* ── Ticker Grid (Home) ───────────────────────────────── */
        .ticker-chip {{
            display: inline-block;
            background-color: {MOCHA["surface0"]};
            border: 1px solid {MOCHA["surface2"]};
            border-radius: 6px;
            padding: 6px 16px;
            margin: 4px;
            font-size: 0.85rem;
            font-weight: 500;
            color: {MOCHA["text"]};
        }}

        /* ── Pipeline Step Cards (Methodology) ────────────────── */
        .pipeline-step {{
            background-color: {MOCHA["surface0"]};
            border: 1px solid {MOCHA["surface2"]};
            border-radius: 8px;
            padding: 16px 20px;
            text-align: center;
        }}

        .pipeline-step .step-num {{
            color: {MOCHA["blue"]};
            font-weight: 600;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }}

        .pipeline-step .step-title {{
            color: {MOCHA["text"]};
            font-weight: 600;
            font-size: 0.95rem;
            margin-top: 4px;
        }}

        .pipeline-step .step-desc {{
            color: {MOCHA["subtext0"]};
            font-size: 0.8rem;
            margin-top: 6px;
            line-height: 1.4;
        }}

        .pipeline-arrow {{
            color: {MOCHA["overlay0"]};
            font-size: 1.2rem;
            text-align: center;
            padding-top: 30px;
        }}

        /* ── Hide Streamlit defaults ──────────────────────────── */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}

        /* ── Scrollbar ────────────────────────────────────────── */
        ::-webkit-scrollbar {{
            width: 8px;
        }}
        ::-webkit-scrollbar-track {{
            background: {MOCHA["mantle"]};
        }}
        ::-webkit-scrollbar-thumb {{
            background: {MOCHA["surface2"]};
            border-radius: 4px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

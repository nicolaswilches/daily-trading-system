import streamlit as st
import plotly.graph_objects as go
import plotly.io as pio

# Catppuccin Mocha Palette
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
    # Load Google Fonts + Material Symbols (for sidebar collapse icon)
    st.markdown(
        """
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">
        """,
        unsafe_allow_html=True,
    )

    # Apply the main stylesheet
    st.markdown(
        f"""
        <style>
        /* ── Base ─────────────────────────────────────────────── */
        .stApp {{
            background-color: {MOCHA["base"]};
            color: {MOCHA["text"]};
            font-family: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
            padding-top: 0.9rem !important;
        }}
        
        /* Reduce top padding on main content */
        .main .block-container {{
            padding-top: 1rem !important;
        }}

        /* ── Typography ───────────────────────────────────────── */
        h1, h2, h3, h4, h5, h6 {{
            color: {MOCHA["text"]};
            font-weight: 600;
            letter-spacing: -0.02em;
            font-family: 'Inter', sans-serif !important;
        }}
        
        h1 {{ font-size: 1.75rem; }}
        h2 {{ font-size: 1.5rem; }}
        h3 {{ font-size: 1.3rem; }}
        h4 {{ font-size: 1.25rem; }}
        h5 {{ font-size: 1.1rem; }}

        p, li, span, label, .stMarkdown, div {{
            color: {MOCHA["subtext1"]};
            font-family: 'Inter', sans-serif;
        }}

        /* Override Streamlit defaults */
        .stMarkdown, .stText, .stCaption {{
            font-family: 'Inter', sans-serif !important;
        }}

        /* ── KPI Cards ────────────────────────────────────────── */
        .kpi-container {{
            background-color: {MOCHA["surface0"]};
            border: 1px solid {MOCHA["surface2"]};
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 16px;
            min-height: 120px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        .kpi-container.square {{
            aspect-ratio: 1;
            min-height: 140px;
            padding: 18px;
        }}

        .kpi-label {{
            font-size: 0.75rem;
            color: {MOCHA["overlay1"]};
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 6px;
            font-weight: 500;
            font-family: 'Inter', sans-serif;
        }}

        .kpi-value {{
            font-size: 1.6rem;
            font-weight: 600;
            color: {MOCHA["text"]};
            line-height: 1.2;
            font-family: 'Inter', sans-serif;
        }}

        .kpi-delta {{
            font-size: 0.85rem;
            margin-top: 4px;
            font-weight: 500;
            font-family: 'Inter', sans-serif;
        }}

        /* ── Feature Cards (Home Page) ────────────────────────── */
        .feature-card {{
            background-color: {MOCHA["surface0"]};
            border: 1px solid {MOCHA["surface2"]};
            border-radius: 10px;
            padding: 32px 28px;
            height: 230px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            overflow: hidden;
        }}

        .feature-card h4 {{
            color: {MOCHA["text"]};
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 12px;
            line-height: 1.3;
            font-family: 'Inter', sans-serif;
        }}

        .feature-card p {{
            color: {MOCHA["subtext0"]};
            font-size: 0.9rem;
            line-height: 1.6;
            flex-grow: 1;
            font-family: 'Inter', sans-serif;
        }}

        /* ── Objective Cards (Home Page) ───────────────────────── */
        .objective-card {{
            background-color: {MOCHA["surface0"]};
            border: 1px solid {MOCHA["surface2"]};
            border-radius: 10px;
            padding: 24px 20px;
            height: 184px;
            display: flex;
            flex-direction: column;
            position: relative;
            overflow: hidden;
        }}

        .objective-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, {MOCHA["blue"]}, {MOCHA["sapphire"]});
        }}

        .objective-card h5 {{
            color: {MOCHA["text"]};
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: 12px;
            font-family: 'Inter', sans-serif;
        }}

        .objective-card p {{
            color: {MOCHA["subtext0"]};
            font-size: 0.85rem;
            line-height: 1.5;
            flex-grow: 1;
            font-family: 'Inter', sans-serif;
        }}

        /* ── Team Cards (Home Page) ───────────────────────────── */
        .team-card {{
            background-color: {MOCHA["surface0"]};
            border: 1px solid {MOCHA["surface2"]};
            border-radius: 10px;
            padding: 24px 16px;
            text-align: center;
            min-height: 160px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }}

        .team-avatar {{
            width: 64px;
            height: 64px;
            border-radius: 50%;
            background-color: {MOCHA["surface1"]};
            border: 2px solid {MOCHA["surface2"]};
            margin-bottom: 12px;
            overflow: hidden;
            flex-shrink: 0;
        }}

        .team-avatar img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}

        .team-card .member-name {{
            color: {MOCHA["text"]};
            font-weight: 600;
            font-size: 0.95rem;
            margin-bottom: 4px;
            font-family: 'Inter', sans-serif;
        }}

        .team-card .member-role {{
            color: {MOCHA["subtext0"]};
            font-size: 0.8rem;
            line-height: 1.3;
            font-family: 'Inter', sans-serif;
        }}

        /* ── Sidebar ──────────────────────────────────────────── */
        [data-testid="stSidebar"] {{
            background-color: {MOCHA["mantle"]};
            border-right: 1px solid {MOCHA["surface0"]};
        }}

        /* Targeted sidebar text styling (replaces wildcard to avoid widget conflicts) */
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] h4,
        [data-testid="stSidebar"] h5,
        [data-testid="stSidebar"] h6,
        [data-testid="stSidebar"] .stMarkdown {{
            color: {MOCHA["subtext1"]};
            font-family: 'Inter', sans-serif;
        }}

        /* Ensure sidebar collapse button uses icon font */
        [data-testid="stSidebarCollapseButton"] span,
        [data-testid="stSidebarCollapseButton"] * {{
            font-family: 'Material Symbols Rounded' !important;
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
            font-family: 'Inter', sans-serif;
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
            font-family: 'Inter', sans-serif;
        }}

        .stButton > button:hover {{
            background-color: {MOCHA["sapphire"]};
        }}

        /* ── Selectbox & Inputs ───────────────────────────────── */
        .stSelectbox > div > div {{
            background-color: {MOCHA["surface0"]};
            border-color: {MOCHA["surface2"]};
            color: {MOCHA["text"]};
            font-family: 'Inter', sans-serif;
        }}

        /* Dropdown popover (rendered as portal outside sidebar) */
        [data-baseweb="popover"] {{
            background-color: {MOCHA["surface0"]} !important;
        }}
        [data-baseweb="popover"] ul {{
            background-color: {MOCHA["surface0"]} !important;
        }}
        [data-baseweb="popover"] li {{
            color: {MOCHA["text"]} !important;
            background-color: {MOCHA["surface0"]} !important;
        }}
        [data-baseweb="popover"] li:hover {{
            background-color: {MOCHA["surface1"]} !important;
        }}
        [data-baseweb="popover"] [aria-selected="true"] {{
            background-color: {MOCHA["surface1"]} !important;
        }}

        /* ── Expanders ────────────────────────────────────────── */
        .streamlit-expanderHeader {{
            background-color: {MOCHA["surface0"]};
            color: {MOCHA["subtext1"]};
            border-radius: 8px;
            font-family: 'Inter', sans-serif;
        }}

        /* ── Dividers ─────────────────────────────────────────── */
        hr {{
            border-color: {MOCHA["surface1"]};
        }}

        /* ── DataFrames ───────────────────────────────────────── */
        .stDataFrame {{
            border: 1px solid {MOCHA["surface1"]};
            border-radius: 8px;
            font-family: 'Inter', sans-serif;
        }}

        /* ── Info / Warning boxes ─────────────────────────────── */
        .stAlert {{
            background-color: {MOCHA["surface0"]};
            border: 1px solid {MOCHA["surface2"]};
            color: {MOCHA["subtext1"]};
            border-radius: 8px;
            font-family: 'Inter', sans-serif;
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
            font-family: 'Inter', sans-serif;
        }}

        /* ── Pipeline Step Cards (Methodology) ────────────────── */
        .pipeline-step {{
            background-color: {MOCHA["surface0"]};
            border: 1px solid {MOCHA["surface2"]};
            border-radius: 8px;
            padding: 24px 32px;
            text-align: center;
            height: 180px;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            min-width: 200px;
        }}

        .pipeline-step .step-num {{
            color: {MOCHA["blue"]};
            font-weight: 600;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-family: 'Inter', sans-serif;
        }}

        .pipeline-step .step-title {{
            color: {MOCHA["text"]};
            font-weight: 600;
            font-size: 1.1rem;
            margin-top: 6px;
            font-family: 'Inter', sans-serif;
        }}

        .pipeline-step .step-desc {{
            color: {MOCHA["subtext0"]};
            font-size: 0.85rem;
            margin-top: 8px;
            line-height: 1.4;
            font-family: 'Inter', sans-serif;
        }}

        .pipeline-arrow {{
            color: {MOCHA["overlay0"]};
            font-size: 1.2rem;
            text-align: center;
            padding-top: 30px;
            font-family: 'Inter', sans-serif;
        }}

        /* ── Home Page Section Spacing ───────────────────────── */
        .home-section {{
            margin-bottom: 3rem !important;
        }}
        
        .home-subsection {{
            margin-bottom: 2rem !important;
        }}

        /* ── Hide Streamlit defaults ──────────────────────────── */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        
        /* Hide keyboard shortcut tooltip */
        [data-testid="stTooltipHoverTarget"] {{
            display: none !important;
        }}
        
        .stTooltip {{
            display: none !important;
        }}

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

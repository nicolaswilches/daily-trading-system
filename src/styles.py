import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* Base Theme */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
        
        .stApp {
            background-color: #FBF9F6;
            color: #1D1917;
            font-family: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif;
        }
        
        /* Headers */
        h1, h2, h3 {
            color: #1D1917;
            font-weight: 600;
            letter-spacing: -0.02em;
        }
        
        /* KPI Cards */
        .kpi-container {
            background-color: #FFFFFF;
            border: 1px solid #EAE2D6;
            border-radius: 8px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }
        
        .kpi-label {
            font-size: 0.85rem;
            color: #6B6661;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 8px;
        }
        
        .kpi-value {
            font-size: 1.8rem;
            font-weight: 600;
            color: #1D1917;
        }
        
        .kpi-delta {
            font-size: 0.9rem;
            margin-top: 4px;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid #EAE2D6;
        }
        
        /* Buttons & Inputs */
        .stButton>button {
            background-color: #1D1917;
            color: white;
            border-radius: 4px;
            border: none;
            padding: 0.5rem 1rem;
        }
        
        /* Hide default Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

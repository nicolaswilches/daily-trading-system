import streamlit as st
from src.styles import apply_custom_style

st.set_page_config(
    page_title="Trading System | Overview",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_style()

def main():
    st.title("Automated Daily Trading System")
    st.markdown("### System Architecture and Strategic Objectives")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        The Automated Daily Trading System is a comprehensive quantitative platform designed to forecast equity market movements. 
        By integrating high-frequency technical indicators with fundamental corporate data, the system provides 
        actionable intelligence for institutional-grade decision making.
        
        #### Core Objectives
        - **Predictive Accuracy:** Utilizing LightGBM models tuned with Bayesian optimization to identify directional probability.
        - **Real-Time Integration:** Seamless connection to the SimFin API for up-to-the-minute market analysis.
        - **Algorithmic Strategy:** Implementation of a rule-based trading engine that converts statistical probabilities into trade execution signals.
        
        #### Methodology
        The platform operates on a dual-objective framework:
        1. **Classification:** Determining the likelihood of a positive price move in the next 24-hour trading session.
        2. **Regression:** Forecasting the magnitude of the log-return to estimate specific price targets.
        """)
        
    with col2:
        st.markdown("""
        <div class="kpi-container">
            <div class="kpi-label">Development Team</div>
            <div style="font-size: 1.1rem; font-weight: 600; margin-bottom: 10px;">Nicolas Wilches</div>
            <div style="color: #6B6661; font-size: 0.9rem;">Lead Data Scientist</div>
            <hr style="border: 0; border-top: 1px solid #EAE2D6; margin: 15px 0;">
            <div class="kpi-label">System Status</div>
            <div style="color: #2D6A4F; font-weight: 600;">Production Ready</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("Select **Market Analysis** in the sidebar to begin real-time forecasting.")

if __name__ == "__main__":
    main()

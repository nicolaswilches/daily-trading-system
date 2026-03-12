import streamlit as st
import joblib
import pandas as pd
import plotly.express as px
from src.styles import apply_custom_style

st.set_page_config(page_title="Methodology", layout="wide")
apply_custom_style()

st.title("Methodology and Model Insights")
st.markdown("Detailed breakdown of the predictive engine and feature engineering hierarchy.")

try:
    clf = joblib.load("models/classifier.joblib")
    features = joblib.load("models/features_list.joblib")

    st.subheader("Feature Importance Analysis")
    st.write("Information gain attribution across the primary feature set.")
    
    importance_df = pd.DataFrame({
        'Feature': features,
        'Importance': clf.feature_importances_
    }).sort_values(by='Importance', ascending=True).tail(15)
    
    fig = px.bar(importance_df, x='Importance', y='Feature', orientation='h',
                 color_discrete_sequence=['#1D1917'])
    
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis_title="Relative Importance (Gain)",
        yaxis_title=""
    )
    
    st.plotly_chart(fig, use_container_width=True)

    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Data Pipeline")
        st.markdown("""
        - **Normalization:** Time-series stationarity is achieved through Log-Return transformations.
        - **Latency:** Point-in-Time alignment ensures no fundamental data is used before its public release date.
        - **Compute:** Polars engine utilized for high-frequency technical indicator calculation.
        """)
        
    with col2:
        st.subheader("Optimization")
        st.markdown("""
        - **Framework:** LightGBM gradient boosting with leaf-wise tree growth.
        - **Tuning:** Optuna Bayesian search conducted over 30 iterations per objective.
        - **Validation:** Five-fold TimeSeriesSplit used to evaluate out-of-sample performance.
        """)

except Exception as e:
    st.error(f"Error loading analytical components: {e}")

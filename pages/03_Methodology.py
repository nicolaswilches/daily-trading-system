import streamlit as st
import joblib
import numpy as np
import pandas as pd
import polars as pl
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import (
    precision_score,
    recall_score,
    accuracy_score,
    f1_score,
    confusion_matrix,
)
from src.styles import apply_custom_style, MOCHA, get_plotly_template

apply_custom_style()

st.title("Methodology & Model Insights")
st.markdown(
    "Detailed breakdown of the predictive engine, validation results, "
    "and feature engineering hierarchy."
)

try:
    clf = joblib.load("models/classifier.joblib")
    features = joblib.load("models/features_list.joblib")
    layout = get_plotly_template()

    # ── Pipeline Overview ─────────────────────────────────────────
    st.markdown("#### Data Pipeline")

    steps = [
        (
            "Step 1",
            "Data Ingestion",
            "Daily prices and quarterly fundamentals from SimFin API",
        ),
        (
            "Step 2",
            "Feature Engineering",
            "70+ technical & fundamental features via Polars",
        ),
        ("Step 3", "Model Training", "LightGBM with Optuna Bayesian optimisation"),
        ("Step 4", "Live Prediction", "Real-time inference on latest market data"),
    ]

    cols = st.columns(len(steps) * 2 - 1)
    for i, (num, title, desc) in enumerate(steps):
        with cols[i * 2]:
            st.markdown(
                f"""
                <div class="pipeline-step">
                    <div class="step-num">{num}</div>
                    <div class="step-title">{title}</div>
                    <div class="step-desc">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        if i < len(steps) - 1:
            with cols[i * 2 + 1]:
                st.markdown(
                    '<div class="pipeline-arrow">→</div>',
                    unsafe_allow_html=True,
                )

    st.divider()

    # ── Model Performance Metrics ─────────────────────────────────
    st.markdown("#### Model Performance")

    try:
        df_all = pl.read_parquet("data/processed/features.parquet")
        # Use all data with TimeSeriesSplit to compute out-of-sample metrics
        # We evaluate on the last fold to reflect the most recent performance
        X_full = df_all.select(features).to_pandas().values
        y_full = df_all["Target_Is_Up"].to_pandas().values

        # Remove rows with NaN targets
        valid_mask = ~np.isnan(y_full)
        X_full = X_full[valid_mask]
        y_full = y_full[valid_mask].astype(int)

        tscv = TimeSeriesSplit(n_splits=5)
        # Get last fold
        for train_idx, test_idx in tscv.split(X_full):
            pass  # iterate to last fold

        X_test = X_full[test_idx]
        y_test = y_full[test_idx]
        y_pred = clf.predict(X_test)

        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, zero_division=0)

        m1, m2, m3, m4 = st.columns(4)
        for col, label, value in [
            (m1, "Precision", f"{precision:.3f}"),
            (m2, "Recall", f"{recall:.3f}"),
            (m3, "Accuracy", f"{accuracy:.3f}"),
            (m4, "F1 Score", f"{f1:.3f}"),
        ]:
            with col:
                st.markdown(
                    f'<div class="kpi-container"><div class="kpi-label">{label}</div>'
                    f'<div class="kpi-value">{value}</div></div>',
                    unsafe_allow_html=True,
                )

        # ── Confusion Matrix ──────────────────────────────────
        st.markdown("##### Confusion Matrix")
        cm = confusion_matrix(y_test, y_pred)
        cm_labels = ["Down (0)", "Up (1)"]

        fig_cm = go.Figure(
            data=go.Heatmap(
                z=cm,
                x=cm_labels,
                y=cm_labels,
                text=cm,
                texttemplate="%{text}",
                textfont=dict(size=16, color=MOCHA["base"]),
                colorscale=[
                    [0, MOCHA["surface1"]],
                    [1, MOCHA["blue"]],
                ],
                showscale=False,
            )
        )
        fig_cm.update_layout(
            layout,
            height=320,
            width=400,
            xaxis_title="Predicted",
            yaxis_title="Actual",
            yaxis=dict(autorange="reversed"),
        )
        st.plotly_chart(fig_cm, use_container_width=False)

    except Exception:
        st.info("Performance metrics require the processed features dataset.")

    st.divider()

    # ── Feature Importance ────────────────────────────────────────
    st.markdown("#### Feature Importance")
    st.markdown("Information-gain attribution across the primary feature set.")

    importance_df = (
        pd.DataFrame({"Feature": features, "Importance": clf.feature_importances_})
        .sort_values("Importance", ascending=True)
        .tail(15)
    )

    fig_imp = px.bar(
        importance_df,
        x="Importance",
        y="Feature",
        orientation="h",
        color_discrete_sequence=[MOCHA["blue"]],
    )
    fig_imp.update_layout(
        layout,
        height=420,
        xaxis_title="Relative Importance (Gain)",
        yaxis_title="",
    )
    st.plotly_chart(fig_imp, use_container_width=True)

    # ── Feature Descriptions ──────────────────────────────────────
    with st.expander("Feature Descriptions"):
        descriptions = {
            "Log_Return_1d": "Logarithmic daily return — captures the relative price change between consecutive sessions.",
            "Dist_SMA_20": "Distance from the 20-day Simple Moving Average — measures short-term trend deviation.",
            "Dist_SMA_50": "Distance from the 50-day SMA — captures medium-term trend positioning.",
            "Dist_SMA_200": "Distance from the 200-day SMA — indicates long-term trend status.",
            "RSI_Proxy": "Relative Strength Index approximation — rolling ratio of up-moves to total moves over 14 days.",
            "Vol_20": "20-day rolling standard deviation of close prices — a volatility measure.",
            "ATR_14": "14-day Average True Range — average daily price range, reflecting volatility.",
            "ROA": "Return on Assets — net income divided by total assets (quarterly fundamental).",
            "Net_Margin": "Net profit margin — net income divided by revenue (quarterly fundamental).",
            "IndustryId": "Numeric industry classification from SimFin.",
            "Volume": "Daily trading volume — the number of shares exchanged.",
            "Number Employees": "Company headcount from SimFin metadata.",
        }
        top_features = importance_df["Feature"].tolist()
        for feat in reversed(top_features):
            desc = descriptions.get(feat, "Derived feature from the ETL pipeline.")
            st.markdown(f"**{feat}** — {desc}")

    st.divider()

    # ── Methodology Details ───────────────────────────────────────
    st.markdown("#### Technical Details")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### Data Sources & Processing")
        st.markdown(
            f"""
            - **Price Data** — 5 years of daily OHLCV from SimFin for 7 US
              large-cap equities.
            - **Fundamentals** — Quarterly income statements and balance
              sheets joined with point-in-time alignment.
            - **Stationarity** — Log-return transformations ensure the target
              series is stationary.
            - **Compute** — Polars engine for high-throughput feature
              calculation on time-series data.
            """
        )

    with col2:
        st.markdown("##### Model & Optimisation")
        st.markdown(
            f"""
            - **Framework** — LightGBM gradient boosting with leaf-wise
              tree growth (classifier + regressor).
            - **Tuning** — Optuna Bayesian search over 30 iterations per
              objective, optimising precision (classifier) and RMSE
              (regressor).
            - **Validation** — 5-fold `TimeSeriesSplit` to prevent data
              leakage and evaluate true out-of-sample performance.
            - **Targets** — Binary direction label (classification) and
              next-day log return (regression).
            """
        )

except Exception as e:
    st.error(f"Error loading analytical components: {e}")

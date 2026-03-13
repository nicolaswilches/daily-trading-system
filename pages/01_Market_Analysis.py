import streamlit as st
import plotly.graph_objects as go
from src.predict import run_prediction
from src.styles import apply_custom_style

st.set_page_config(page_title="Market Analysis", layout="wide")
apply_custom_style()

# 1. Sidebar Configuration
tickers = ["AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "NVDA", "META"]
selected_ticker = st.sidebar.selectbox("Select Asset", tickers)

# Auto-execute on selection
if selected_ticker:
    with st.spinner(f"Analyzing {selected_ticker}..."):
        result = run_prediction(selected_ticker)
        
        if "error" in result:
            st.error(result["error"])
        else:
            # Header with Logo
            col_head1, col_head2 = st.columns([0.1, 5])
            with col_head1:
                # Use Clearbit for logos
                logo_ticker = selected_ticker.lower()
                if selected_ticker == "GOOG": logo_url = "https://logo.clearbit.com/google.com"
                elif selected_ticker == "META": logo_url = "https://logo.clearbit.com/meta.com"
                else: logo_url = f"https://logo.clearbit.com/{logo_ticker}.com"
                st.image(logo_url, width=60)
            with col_head2:
                st.title(f"{selected_ticker} Analysis")
                st.markdown(f"Last updated: {result['last_updated']}")

            # KPI Cards
            k1, k2, k3, k4, k5 = st.columns(5)
            
            with k1:
                st.markdown(f"""
                <div class="kpi-container">
                    <div class="kpi-label">Current Price</div>
                    <div class="kpi-value">${result['current_price']:.2f}</div>
                    <div class="kpi-delta" style="color: {'#2D6A4F' if result['change_pct'] >= 0 else '#A4161A'};">
                        {'+' if result['change_pct'] >= 0 else ''}{result['change_pct']:.2f}%
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with k2:
                st.markdown(f"""<div class="kpi-container"><div class="kpi-label">Day High</div><div class="kpi-value">${result['high']:.2f}</div></div>""", unsafe_allow_html=True)
            with k3:
                st.markdown(f"""<div class="kpi-container"><div class="kpi-label">Day Low</div><div class="kpi-value">${result['low']:.2f}</div></div>""", unsafe_allow_html=True)
            with k4:
                st.markdown(f"""<div class="kpi-container"><div class="kpi-label">Volume</div><div class="kpi-value">{result['volume']/1e6:.1f}M</div></div>""", unsafe_allow_html=True)
            with k5:
                st.markdown(f"""<div class="kpi-container"><div class="kpi-label">Target Price</div><div class="kpi-value">${result['target_price']:.2f}</div></div>""", unsafe_allow_html=True)

            # Signal Section
            st.subheader("Algorithmic Trading Signal")
            sig_color = "#2D6A4F" if result['signal'] == "BUY" else "#A4161A" if result['signal'] == "SELL" else "#6B6661"
            st.markdown(f"""
            <div style="background-color: {sig_color}10; border: 1px solid {sig_color}; padding: 20px; border-radius: 8px;">
                <h2 style="color: {sig_color}; margin: 0;">{result['signal']}</h2>
                <div style="color: {sig_color}; font-size: 0.9rem;">Model Confidence: {result['prob_up']*100:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)

            st.divider()

            # Historical Charts
            st.subheader("Market History")
            hist = result["history"].tail(100).to_pandas() # Last 100 days for clarity
            
            tab1, tab2 = st.tabs(["Candlestick", "Line Chart"])
            
            with tab1:
                fig_candle = go.Figure(data=[go.Candlestick(
                    x=hist['Date'],
                    open=hist['Open'], high=hist['High'],
                    low=hist['Low'], close=hist['Close'],
                    increasing_line_color='#2D6A4F', decreasing_line_color='#A4161A'
                )])
                fig_candle.update_layout(
                    template="plotly_white",
                    margin=dict(l=0, r=0, t=0, b=0),
                    height=450,
                    xaxis_rangeslider_visible=False
                )
                st.plotly_chart(fig_candle, use_container_width=True)
                
            with tab2:
                fig_line = go.Figure(data=go.Scatter(
                    x=hist['Date'], y=hist['Close'],
                    mode='lines', line=dict(color='#1D1917', width=2)
                ))
                fig_line.update_layout(
                    template="plotly_white",
                    margin=dict(l=0, r=0, t=0, b=0),
                    height=450
                )
                st.plotly_chart(fig_line, use_container_width=True)

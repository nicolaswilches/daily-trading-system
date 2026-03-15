import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from src.predict import run_prediction
from src.styles import apply_custom_style, MOCHA, get_plotly_template

apply_custom_style()

# ── Sidebar ───────────────────────────────────────────────────────────
tickers = ["AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "NVDA", "META"]
selected_ticker = st.sidebar.selectbox("Select Asset", tickers)

if selected_ticker:
    with st.spinner(f"Analyzing {selected_ticker}..."):
        result = run_prediction(selected_ticker)

        if "error" in result:
            st.error(result["error"])
        else:
            # ── Header ────────────────────────────────────────────
            col_h1, col_h2 = st.columns([0.08, 5])
            with col_h1:
                logo_ticker = selected_ticker.lower()
                if selected_ticker == "GOOG":
                    logo_url = "https://logo.clearbit.com/google.com"
                elif selected_ticker == "META":
                    logo_url = "https://logo.clearbit.com/meta.com"
                else:
                    logo_url = f"https://logo.clearbit.com/{logo_ticker}.com"
                st.image(logo_url, width=52)
            with col_h2:
                st.title(f"{selected_ticker} Analysis")
                st.caption(f"Last updated: {result['last_updated']}")

            # ── KPI Cards ─────────────────────────────────────────
            k1, k2, k3, k4, k5 = st.columns(5)

            change_color = MOCHA["green"] if result["change_pct"] >= 0 else MOCHA["red"]
            change_sign = "+" if result["change_pct"] >= 0 else ""

            with k1:
                st.markdown(
                    f"""
                    <div class="kpi-container">
                        <div class="kpi-label">Current Price</div>
                        <div class="kpi-value">${result["current_price"]:.2f}</div>
                        <div class="kpi-delta" style="color: {change_color};">
                            {change_sign}{result["change_pct"]:.2f}%
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with k2:
                st.markdown(
                    f'<div class="kpi-container"><div class="kpi-label">Day High</div>'
                    f'<div class="kpi-value">${result["high"]:.2f}</div></div>',
                    unsafe_allow_html=True,
                )
            with k3:
                st.markdown(
                    f'<div class="kpi-container"><div class="kpi-label">Day Low</div>'
                    f'<div class="kpi-value">${result["low"]:.2f}</div></div>',
                    unsafe_allow_html=True,
                )
            with k4:
                st.markdown(
                    f'<div class="kpi-container"><div class="kpi-label">Volume</div>'
                    f'<div class="kpi-value">{result["volume"] / 1e6:.1f}M</div></div>',
                    unsafe_allow_html=True,
                )
            with k5:
                st.markdown(
                    f'<div class="kpi-container"><div class="kpi-label">Target Price</div>'
                    f'<div class="kpi-value">${result["target_price"]:.2f}</div></div>',
                    unsafe_allow_html=True,
                )

            # ── Trading Signal ────────────────────────────────────
            signal = result["signal"]
            if signal == "BUY":
                sig_color = MOCHA["green"]
            elif signal == "SELL":
                sig_color = MOCHA["red"]
            else:
                sig_color = MOCHA["yellow"]

            st.markdown(
                f"""
                <div class="signal-banner"
                     style="background-color: {sig_color}12;
                            border: 1px solid {sig_color};">
                    <h2 style="color: {sig_color};">{signal}</h2>
                    <span class="conf" style="color: {sig_color};">
                        Model Confidence: {result["prob_up"] * 100:.1f}%
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            with st.expander("How is the signal determined?"):
                st.markdown(
                    f"""
                    The LightGBM classifier outputs a probability that the
                    stock's price will increase in the next trading session.

                    | Probability | Signal |
                    |---|---|
                    | > 55 % | **BUY** |
                    | 45 – 55 % | **HOLD** |
                    | < 45 % | **SELL** |

                    The **confidence** value shown is the model's raw
                    probability of an upward move.  A companion regression
                    model estimates the expected magnitude and derives the
                    **Target Price**.
                    """
                )

            st.divider()

            # ── Historical Charts ─────────────────────────────────
            st.markdown("#### Market History")
            hist = result["history"].tail(100).to_pandas()
            layout = get_plotly_template()

            tab1, tab2 = st.tabs(["Candlestick + Volume", "Price + Moving Averages"])

            with tab1:
                fig = make_subplots(
                    rows=2,
                    cols=1,
                    shared_xaxes=True,
                    row_heights=[0.75, 0.25],
                    vertical_spacing=0.03,
                )
                fig.add_trace(
                    go.Candlestick(
                        x=hist["Date"],
                        open=hist["Open"],
                        high=hist["High"],
                        low=hist["Low"],
                        close=hist["Close"],
                        increasing_line_color=MOCHA["green"],
                        decreasing_line_color=MOCHA["red"],
                        increasing_fillcolor=MOCHA["green"],
                        decreasing_fillcolor=MOCHA["red"],
                        name="OHLC",
                    ),
                    row=1,
                    col=1,
                )
                # Volume bars
                colors = [
                    MOCHA["green"] if c >= o else MOCHA["red"]
                    for c, o in zip(hist["Close"], hist["Open"])
                ]
                fig.add_trace(
                    go.Bar(
                        x=hist["Date"],
                        y=hist["Volume"],
                        marker_color=colors,
                        opacity=0.5,
                        name="Volume",
                        showlegend=False,
                    ),
                    row=2,
                    col=1,
                )
                fig.update_layout(
                    layout,
                    height=520,
                    xaxis_rangeslider_visible=False,
                    xaxis2=dict(
                        gridcolor=MOCHA["surface1"],
                        linecolor=MOCHA["surface1"],
                        tickfont=dict(color=MOCHA["subtext0"]),
                    ),
                    yaxis2=dict(
                        gridcolor=MOCHA["surface1"],
                        linecolor=MOCHA["surface1"],
                        tickfont=dict(color=MOCHA["subtext0"]),
                    ),
                    showlegend=False,
                    hovermode="x unified",
                )
                # Spike lines for crosshair
                fig.update_xaxes(
                    spikemode="across",
                    spikethickness=1,
                    spikecolor=MOCHA["overlay0"],
                    spikesnap="cursor",
                )
                fig.update_yaxes(
                    spikemode="across",
                    spikethickness=1,
                    spikecolor=MOCHA["overlay0"],
                    spikesnap="cursor",
                )
                st.plotly_chart(fig, use_container_width=True)

            with tab2:
                fig_line = go.Figure()
                # Close price
                fig_line.add_trace(
                    go.Scatter(
                        x=hist["Date"],
                        y=hist["Close"],
                        mode="lines",
                        name="Close",
                        line=dict(color=MOCHA["text"], width=2),
                    )
                )
                # SMA overlays
                for window, color, label in [
                    (20, MOCHA["blue"], "SMA 20"),
                    (50, MOCHA["peach"], "SMA 50"),
                ]:
                    col_name = f"sma_{window}"
                    hist[col_name] = hist["Close"].rolling(window).mean()
                    fig_line.add_trace(
                        go.Scatter(
                            x=hist["Date"],
                            y=hist[col_name],
                            mode="lines",
                            name=label,
                            line=dict(color=color, width=1.5, dash="dot"),
                        )
                    )
                fig_line.update_layout(
                    layout,
                    height=480,
                    hovermode="x unified",
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="left",
                        x=0,
                    ),
                )
                fig_line.update_xaxes(
                    spikemode="across",
                    spikethickness=1,
                    spikecolor=MOCHA["overlay0"],
                    spikesnap="cursor",
                )
                fig_line.update_yaxes(
                    spikemode="across",
                    spikethickness=1,
                    spikecolor=MOCHA["overlay0"],
                    spikesnap="cursor",
                )
                st.plotly_chart(fig_line, use_container_width=True)

            # ── Recent Data Table ─────────────────────────────────
            with st.expander("Recent Price Data"):
                table_cols = ["Date", "Open", "High", "Low", "Close", "Volume"]
                available = [c for c in table_cols if c in hist.columns]
                recent = hist[available].tail(15).sort_values("Date", ascending=False)
                recent["Volume"] = recent["Volume"].apply(
                    lambda v: f"{v / 1e6:.1f}M" if v >= 1e6 else f"{v:,.0f}"
                )
                for col in ["Open", "High", "Low", "Close"]:
                    if col in recent.columns:
                        recent[col] = recent[col].apply(lambda x: f"${x:.2f}")
                st.dataframe(recent, use_container_width=True, hide_index=True)

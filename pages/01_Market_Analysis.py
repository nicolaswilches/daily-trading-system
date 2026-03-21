import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from src.predict import run_prediction
from src.styles import apply_custom_style, MOCHA, get_plotly_template

apply_custom_style()

# Company info
TICKER_INFO = {
    "AAPL": {"name": "Apple Inc.", "logo": "assets/logos/AAPL.png"},
    "MSFT": {"name": "Microsoft Corporation", "logo": "assets/logos/MSFT.png"},
    "AMZN": {"name": "Amazon.com Inc.", "logo": "assets/logos/AMZN.png"},
    "TSLA": {"name": "Tesla Inc.", "logo": "assets/logos/TSLA.png"},
    "NVDA": {"name": "NVIDIA Corporation", "logo": "assets/logos/NVDA.png"}
}

# ── Sidebar ───────────────────────────────────────────────────────────
tickers = ["AAPL", "MSFT", "AMZN", "TSLA", "NVDA"]
selected_ticker = st.sidebar.radio("Select Asset", tickers)

if selected_ticker:
    with st.spinner(f"Analyzing {selected_ticker}..."):
        result = run_prediction(selected_ticker)

        if "error" in result:
            st.error(result["error"])
        else:
            # Resolve company info before columns so both sides can use it
            company_info = TICKER_INFO.get(
                selected_ticker, {"name": f"{selected_ticker} Corporation"}
            )

            # ── Header ────────────────────────────────────────────
            col_left, col_spacer, col_right = st.columns([5, 3, 1])

            with col_left:
                st.title(selected_ticker)
                st.markdown(f"**{company_info['name']}**")
                st.caption(f"Last updated: {result['last_updated']}")

            with col_right:
                logo_path = company_info.get("logo", "")
                if logo_path:
                    st.image(logo_path, width=70)

            # ── Square KPI Cards with Color Highlighting ─────────
            k1, k2, k3, k4, k5, k6 = st.columns(6)

            # Signal card
            signal = result["signal"]
            if signal == "BUY":
                sig_color = MOCHA["green"]
                sig_bg = "rgba(166, 227, 161, 0.12)"
            elif signal == "SELL":
                sig_color = MOCHA["red"]
                sig_bg = "rgba(243, 139, 168, 0.12)"
            else:
                sig_color = MOCHA["yellow"]
                sig_bg = "rgba(249, 226, 175, 0.12)"

            with k1:
                st.markdown(
                    f"""
                    <div class="kpi-container square" style="border-color: {sig_color}; 
                                                           border-width: 2px;
                                                           background-color: {sig_bg};">
                        <div class="kpi-label">Signal</div>
                        <div class="kpi-value" style="color: {sig_color}; font-size: 1.4rem;">{signal}</div>
                        <div class="kpi-delta" style="color: {sig_color};">
                            {result["prob_up"] * 100:.1f}%
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # Current Price with day-over-day change and highlighting
            change_pct = float(result.get("change_pct", 0))
            change_color = MOCHA["green"] if change_pct >= 0 else MOCHA["red"]
            change_bg = (
                "rgba(166, 227, 161, 0.08)"
                if change_pct >= 0
                else "rgba(243, 139, 168, 0.08)"
            )
            change_sign = "+" if change_pct >= 0 else ""

            with k2:
                st.markdown(
                    f"""
                    <div class="kpi-container square" style="background-color: {change_bg}; 
                                                           border-color: {change_color}; 
                                                           border-width: 2px;">
                        <div class="kpi-label">Current Price</div>
                        <div class="kpi-value">${result["current_price"]:.2f}</div>
                        <div class="kpi-delta" style="color: {change_color};">
                            {change_sign}{change_pct:.2f}%
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with k3:
                st.markdown(
                    f"""
                    <div class="kpi-container square">
                        <div class="kpi-label">Day High</div>
                        <div class="kpi-value">${result["high"]:.2f}</div>
                        <div class="kpi-delta" style="color: {MOCHA["subtext0"]};">
                            Session high
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with k4:
                st.markdown(
                    f"""
                    <div class="kpi-container square">
                        <div class="kpi-label">Day Low</div>
                        <div class="kpi-value">${result["low"]:.2f}</div>
                        <div class="kpi-delta" style="color: {MOCHA["subtext0"]};">
                            Session low
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # Handle volume conversion safely
            volume = float(result.get("volume", 0))

            with k5:
                st.markdown(
                    f"""
                    <div class="kpi-container square">
                        <div class="kpi-label">Volume</div>
                        <div class="kpi-value">{volume / 1e6:.1f}M</div>
                        <div class="kpi-delta" style="color: {MOCHA["subtext0"]};">
                            Shares traded
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with k6:
                st.markdown(
                    f"""
                    <div class="kpi-container square">
                        <div class="kpi-label">Target Price</div>
                        <div class="kpi-value">${result["target_price"]:.2f}</div>
                        <div class="kpi-delta" style="color: {MOCHA["subtext0"]};">
                            Model prediction
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.divider()

            # ── Historical Charts ─────────────────────────────────
            st.markdown("#### Market History")

            # Handle history data safely
            if hasattr(result["history"], "tail"):
                hist = result["history"].tail(100).to_pandas()
            else:
                st.error("Unable to load historical data for charting.")
                st.stop()

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

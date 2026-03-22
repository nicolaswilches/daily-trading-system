# [Automated Daily Trading System](https://nicolaswilches-daily-trading-system-main-2ez8iq.streamlit.app/)

![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python&logoColor=white)
![uv](https://img.shields.io/badge/uv-package%20manager-blueviolet)
![LightGBM](https://img.shields.io/badge/LightGBM-gradient%20boosting-green)
![Streamlit](https://img.shields.io/badge/Streamlit-dashboard-red?logo=streamlit)

A quantitative trading pipeline that forecasts next-day stock price direction and magnitude for major US equities. Combines two LightGBM models (classification + regression) with a live Streamlit dashboard for real-time signal generation and strategy backtesting.

---

## Overview

The system is structured as two cooperating modules:

1. **Offline Pipeline:** Ingests 5 years of historical OHLCV and corporate fundamentals from SimFin, engineers 70+ features with Polars, and trains two LightGBM models optimized via Optuna Bayesian search.
2. **Live Dashboard:** A Streamlit application that fetches real-time data, runs inference, displays trading signals, and simulates historical strategy performance against a buy-and-hold benchmark.

**Core stack:** Polars, scikit-learn, scikit-learn, Optuna, Streamlit, SimFin API

---

## Pipeline Architecture

```text
SimFin API
    │
    ▼
src/fetch_data.py  ──►  data/raw/  (prices, fundamentals — Parquet)
    │
    ▼
src/etl.py  ──►  data/processed/features.parquet  (70+ engineered features)
    │
    ▼
src/train.py  ──►  models/  (classifier.joblib · regressor.joblib · features_list.joblib)
    │
    ▼
src/predict.py  +  SimFin API (live)
    │
    ▼
Streamlit Dashboard  (main.py + pages/)
```

---

## Project Structure

```text
daily-trading-system/
├── .env.example              # Required environment variables template
├── .streamlit/
│   └── config.toml           # Streamlit theme (Catppuccin Mocha)
├── assets/
│   └── logos/                # Company logo assets (PNG/SVG)
├── data/
│   ├── raw/                  # Ingested CSVs and Parquet files (gitignored)
│   └── processed/
│       └── features.parquet  # Engineered feature set
├── docs/
│   ├── AI_USAGE_LOG.md       # AI collaboration log
│   └── executive_summary.md  # Project vision and approach
├── models/
│   ├── classifier.joblib     # Trained LightGBM classifier
│   ├── regressor.joblib      # Trained LightGBM regressor
│   └── features_list.joblib  # Feature column order for inference
├── notebooks/
│   ├── etl_pipeline_v1.ipynb     # ETL prototyping
│   └── model_exploration.ipynb   # Model experimentation
├── pages/
│   ├── 00_Home.py            # Landing page
│   ├── 01_Market_Analysis.py # Live signal dashboard
│   ├── 02_Trading_Strategy.py# Backtesting engine
│   └── 03_Methodology.py     # Model insights and validation
├── scripts/
│   ├── debug_tickers.py      # Ticker mapping diagnostic
│   └── test_api.py           # API authentication diagnostic
├── src/
│   ├── api_wrapper.py        # SimFin API v3 client (OOP, rate-limited)
│   ├── etl.py                # Feature engineering pipeline
│   ├── fetch_data.py         # Data ingestion from SimFin
│   ├── predict.py            # Real-time inference engine
│   ├── styles.py             # Custom CSS and Plotly theming
│   └── train.py              # Model training and hyperparameter tuning
├── main.py                   # Streamlit entry point
├── pyproject.toml            # Dependencies and project metadata (uv)
└── requirements.txt          # Pinned dependencies (alternative to uv)
```

---

## Quick Start

**Prerequisites:** Python 3.12+, [`uv`](https://docs.astral.sh/uv/), and a [SimFin API key](https://simfin.com/).

```bash
# 1. Clone the repository
git clone <repo-url>
cd daily-trading-system

# 2. Configure environment
cp .env.example .env
# Edit .env and set your SIMFIN_API_KEY

# 3. Install dependencies
uv sync
```

---

## Running the Pipeline

Run each step in order to reproduce the full pipeline from raw data to trained models.

```bash
# Step 1 — Ingest data from SimFin API (downloads ~5 years of prices + fundamentals)
uv run src/fetch_data.py

# Step 2 — Engineer features (point-in-time joins, technical indicators, fundamentals)
uv run src/etl.py

# Step 3 — Train and optimize both models via Optuna Bayesian search
uv run src/train.py
```

Pre-trained models are already included in `models/` — steps 1–3 are only needed to retrain.

---

## Running the Dashboard

```bash
uv run streamlit run main.py
```

The app will open at `http://localhost:8501`. Four pages are available:

| Page | Description |
| --- | --- |
| Home | Project overview and feature summary |
| Market Analysis | Live trading signals for selected tickers |
| Trading Strategy | Interactive backtesting with configurable parameters |
| Methodology | Model validation metrics and feature importance |

---

## Feature Engineering

The ETL pipeline generates 70+ features from daily price data and quarterly fundamentals:

| Category | Features |
| --- | --- |
| **Trend** | Distance from SMA-20, SMA-50, SMA-200 |
| **Momentum** | RSI proxy, 1-day log return |
| **Volatility** | Bollinger Band width (20-day rolling std), ATR-14 |
| **Fundamentals** | Return on Assets (ROA), Net Margin |

**Anti-leakage design:** fundamentals are aligned to prices using point-in-time joins (no future data seen during training). Validation uses 5-fold `TimeSeriesSplit` to respect temporal ordering.

---

## Model Architecture

Two LightGBM models are trained independently, each tuned with 30 Optuna trials:

| Model | Objective | Metric | Output |
| --- | --- | --- | --- |
| **Classifier** | Binary up/down direction | Precision (minimize false buys) | `prob_up` ∈ [0, 1] |
| **Regressor** | Next-day log-return magnitude | RMSE | `pred_log_return` |

**Signal generation:**

- `BUY` — `prob_up > 0.55`
- `SELL` — `prob_up < 0.45`
- `HOLD` — otherwise

**Target price:** `current_price × exp(pred_log_return)`

---

## Data Sources

- **Provider:** [SimFin](https://simfin.com/) — free-tier API (daily prices + quarterly fundamentals)
- **Coverage:** 5 years of historical data
- **Tickers:** AAPL, MSFT, AMZN, TSLA, NVDA

---

## Financial Disclaimer

This project is developed for **educational and research purposes only**. The signals and predictions generated by this system do not constitute financial advice. Past performance of any strategy does not guarantee future results. Always consult a qualified financial advisor before making investment decisions.

---

## Authors

Nicolás Higuera, Gilles Hamers, Madelyn Ehni, Salah Mneimne, Alberto Cabezudo

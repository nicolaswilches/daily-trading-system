# Automated Daily Trading System

A professional quantitative trading platform that integrates real-time financial data with machine learning to forecast stock market movements. This system identifies directional probabilities and specific price targets for major US equities using a dual-objective LightGBM framework.

## Overview

This project is divided into two primary modules:
1. **Data Analytics Module**: An offline pipeline that processes 5 years of historical prices and corporate fundamentals using **Polars**, followed by model optimization using **LightGBM** and **Optuna**.
2. **Web-Based Trading System**: A real-time **Streamlit** dashboard that connects to the **SimFin API** to provide live predictive signals and backtesting simulations.

## Project Structure

```text
├── data/               # Raw and processed datasets (Parquet format)
├── models/             # Serialized LightGBM models and feature metadata
├── notebooks/          # ETL prototypes and model exploration
├── pages/              # Streamlit multi-page application components
├── src/                
│   ├── api_wrapper.py  # Object-oriented SimFin API v3 client
│   ├── etl.py          # Automated data transformation pipeline
│   ├── predict.py      # Real-time inference engine
│   ├── styles.py       # Anthropic-inspired UI theme injection
│   └── train.py        # Model training and Bayesian optimization
├── main.py             # Streamlit application entry point
├── pyproject.toml      # Project dependencies and metadata (uv)
└── README.md           # Project documentation
```

## Setup & Installation

This project uses `uv` for high-performance dependency management.

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd daily-trading-system
   ```

2. **Configure Environment:**
   Create a `.env` file in the root directory and add your SimFin API Key:
   ```text
   SIMFIN_API_KEY=your_api_key_here
   ```

3. **Install Dependencies:**
   ```bash
   uv sync
   ```

## Usage

### 1. Data Pipeline & Training
To re-run the full analytical pipeline (Fetch -> ETL -> Train):
```bash
uv run src/fetch_data.py
uv run src/etl.py
uv run src/train.py
```

### 2. Launch the Dashboard
To start the interactive Streamlit application:
```bash
uv run streamlit run main.py
```

## Methodology

### Indicator Battery
The system utilizes 70+ features across four categories:
- **Trend:** Multi-window SMAs (20, 50, 200).
- **Momentum:** RSI and Log-Return vectors.
- **Volatility:** Bollinger Band width and ATR (Average True Range).
- **Fundamentals:** ROA, Net Margin, and Enterprise Metadata.

### Model Architecture
- **Classification:** LightGBM optimized for **Precision** to minimize false-buy signals.
- **Regression:** LightGBM optimized for **RMSE** on Log-Returns to provide realistic price targets.
- **Validation:** 5-fold TimeSeriesSplit to prevent data leakage and ensure temporal robustness.

## Development Team
- **Nicolas Wilches** - Lead Data Scientist & System Architect

---
*Developed for the Data Science Group Assignment.*

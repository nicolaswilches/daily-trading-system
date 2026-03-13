# Executive Summary: Automated Daily Trading System

## Project Vision
The financial markets generate vast amounts of data daily, yet converting this raw information into actionable trading intelligence remains a complex challenge. This project delivers a production-ready, automated trading system that leverages machine learning to forecast short-term equity movements with institutional-grade precision.

## Strategic Approach

### 1. Data Integrity and Engineering
The foundation of the system is a high-performance ETL (Extract, Transform, Load) pipeline built with **Polars**. We processed over 5 years of historical data for 7 major US equities, integrating:
- **Technical Indicators:** A battery of momentum and trend metrics (RSI, MACD, SMAs).
- **Fundamental Insights:** Quarterly corporate health metrics (ROA, Net Margin) aligned precisely with public release dates to eliminate predictive bias.

### 2. Machine Learning Framework
We implemented a dual-objective model using the **LightGBM** gradient boosting framework:
- **Directional Engine:** A classifier optimized to predict the probability of a positive price move.
- **Valuation Engine:** A regressor that forecasts the specific magnitude of expected returns.
The models were tuned using **Optuna** (Bayesian Optimization) and validated via **TimeSeriesSplit** to ensure they perform reliably across different market regimes.

### 3. User Experience and Real-Time Delivery
The final output is a minimal, high-fidelity **Streamlit** dashboard inspired by modern fintech aesthetics. It provides users with:
- **Market Analysis:** Live price targets and directional signals.
- **Trading Strategy:** A backtesting environment to visualize strategy performance against standard market benchmarks.
- **Methodology Transparency:** A clear breakdown of the factors driving the AI’s decisions.

## Challenges and Solutions
- **API Connectivity:** Navigating the specific authentication requirements of the SimFin API required iterative diagnostic cycles. We successfully implemented a robust v3 client with built-in rate-limiting and ticker mapping.
- **Overfitting Prevention:** Given the noise in financial data, we prioritized regularization and temporal validation to ensure our signals are statistically significant rather than coincidental.

## Conclusion
The Automated Daily Trading System demonstrates that by combining modern data processing tools with advanced gradient boosting models, it is possible to build a robust framework for market forecasting. The system is scalable, transparent, and ready for deployment in a live trading environment.

---
**Lead Data Scientist:** Nicolas Wilches  
**Date:** March 2026

# Daily Trading System — Executive Summary

## Project Overview

This project is a proof of concept of a daily trading system, structured as an end-to-end machine learning pipeline built on Python. This project is structured in two main phases:

The first, a data analytics module composed of an ETL process to extract and prepare data for analysis, machine learning models to predict market movements, and a trading strategy based on those predictions.

The second is a web-based trading application built on Streamlit. This application integrates our trained machine learning models and SimFin's data to provide users with a seamless experience to analyze the financial markets.

In the following sections we discuss in detail the data sources used, our ETL process, the models considered and their selection criteria, the web application architecture, challenges faced, and final conclusions.

---

## Data Sources

Our system relies on two types of financial data, both sourced from **SimFin**, a financial data provider that offers free access to US market data through an API:

- **Daily Stock Prices:** Five years of historical open, high, low, close, and volume data for five major US equities — Apple (AAPL), Microsoft (MSFT), Amazon (AMZN), Tesla (TSLA), and NVIDIA (NVDA). This data serves as the foundation for identifying price trends and computing technical indicators.

- **Quarterly Financial Statements:** Income statements and balance sheets published by each company every quarter. These reports contain key health metrics,  such as profitability and return on assets, that reflect the underlying business performance behind each stock price.

Combining both types of data allows our models to look beyond short-term trends and incorporate the financial fundamentals of each company in their predictions.

---

## ETL Process

Before analyzing the data or building our model, we needed to clean, structure, and enrich the raw data extracted. This process referred to as ETL (Extract, Transform, Load) is a critical foundation for the reliability of our trading system.

**Extract:** Data is downloaded automatically from the SimFin API and stored locally in an efficient binary format (Parquet) for fast processing.

**Transform:** This is the most important step. We engineered over 70 features,  measurable signals derived from raw data that the model uses to deliver predictions. These fall into four categories:

- *Trend indicators:* Prices moving above or below their historical averages over different time windows (20, 50, and 200 trading days).
- *Momentum indicators:* How fast is the price moving, and is it gaining or losing strength?
- *Volatility indicators:* How much is the price fluctuating day-to-day?
- *Fundamental indicators:* Is the company becoming more or less profitable over time?

A critical design decision in this step was ensuring that quarterly financial data is only made available to the model from the date it was *publicly released*, never in advance. This prevents the model from "cheating" by learning from information that would not have been available to an investor at the time of a trade.

**Load:** The final, enriched dataset is saved and made available to the model training stage.

---

## Model Selection

Our goal was to build a system that answers two questions for each stock on any given day: **will the price go up or down tomorrow?** and **by how much?**

We considered multiple approaches, ranging from simple linear models to more complex machine learning algorithms. We ultimately selected **LightGBM**, a gradient boosting framework, for the following reasons:

- **Performance on tabular data:** LightGBM consistently outperforms simpler models when working with structured, feature-rich datasets like ours. It is capable of learning complex, non-linear patterns that linear regression would miss.
- **Speed and efficiency:** It trains significantly faster than comparable algorithms, which was important given the volume of data and the number of model configurations we needed to test.
- **Interpretability:** Unlike black-box models, LightGBM allows us to inspect which features are driving predictions, a key requirement for a transparent trading system.

We trained two models independently:

1. **Direction Model (Classifier):** Predicts the probability that a stock's price will rise the next day. This model is configureg to limit false buy signals, we prefer to miss an opportunity rather than act on a wrong signal.
2. **Magnitude Model (Regressor):** Estimates how large the expected price move will be. This is used to generate a price target for each prediction.

To ensure the models generalize to new data and are not simply memorizing historical patterns, we used a technique called **time-series cross-validation** — always training on the past and testing on the future, never the reverse.

Model configurations were optimized automatically using **Optuna**, a hyperparameter tuning framework that searches for the best model settings through Bayesian optimization, rather than manual trial and error.

---

## Web Application Architecture

The final product is a four-page interactive dashboard built with Streamlit, designed to allow users to leverage the outputs of our machine learning models through an intuitive interface.

The application is structured around two operating modes:

**Offline Pipeline (runs once, or as needed):** Data is ingested, features are engineered, and models are trained. The resulting models are saved to disk and do not need to be retrained every time the app is opened.

**Live Dashboard (runs in real time):** The trained models are loaded and combined with fresh market data fetched from the SimFin API to generate up-to-date predictions. This happens on demand each time a user opens the app.

The four pages serve distinct purposes:

| Page | Purpose |
| --- | --- |
| **Home** | Introduction to the system and its objectives |
| **Market Analysis** | Live trading signals (Buy / Hold / Sell) and price targets for the five covered stocks |
| **Trading Strategy** | A backtesting simulator that shows how the system's signals would have performed historically, compared to a simple buy-and-hold strategy |
| **Methodology** | A transparent breakdown of the model's performance metrics and the most influential predictive factors |

---

## Challenges

**API Integration:** Connecting to the SimFin API required navigating version-specific authentication requirements (v1 vs. v3) and subtle differences in how ticker symbols were handled across data endpoints. Resolving these issues required iterative diagnostic work.

**Preventing Data Leakage:** Financial datasets present a subtle but critical challenge: quarterly reports are published with a delay after the period they cover. Using this data without accounting for publication dates would mean the model "knows the future" during training, inflating performance metrics artificially. We implemented point-in-time alignment to ensure only publicly available information was used at each point in the historical record.

**Balancing Signal Precision:** Financial markets are inherently noisy, and not every pattern in historical data reflects a genuine, repeatable signal. We deliberately optimized the direction model for precision over recall, meaning the system would rather issue fewer, higher-confidence signals than generate a large number of uncertain predictions.

**Team Collaboration:** As a distributed team working across different environments, coordinating development through GitHub, managing branches, pull requests, and shared dependencies required clear conventions and communication to avoid conflicts and data inconsistencies.

---

## Conclusions

The Automated Daily Trading System demonstrates that a well-structured end-to-end machine learning pipeline can produce interpretable, real-time trading intelligence from publicly available financial data.

By combining price history with corporate fundamentals, applying rigorous data validation practices, and building a transparent user interface, the system delivers both predictive capability and stakeholder trust.

This project is a proof of concept. The models are trained on historical data and do not guarantee future performance. The signals generated are intended for research and educational purposes only and should not be treated as financial advice.

Looking ahead, the system could be extended in several directions: incorporating additional asset classes, adding macroeconomic indicators, or deploying the application to a cloud environment for broader access.
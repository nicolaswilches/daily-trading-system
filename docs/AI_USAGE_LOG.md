# AI Usage Log

This document records the collaborative development process between the Lead Data Scientist and the Gemini CLI (AI Assistant).

## AI Tools Used

- **Tool:** Gemini CLI (Powered by Google Gemini models)
- **Primary Tasks:** Code generation, debugging, architectural design, and UI/UX styling.

## Task Breakdown

| Task | AI Contribution | Outcome |
|---|---|---|
| **ETL Pipeline** | Generated high-performance Polars code for multi-ticker processing and fundamental data merging. | Successfully implemented a "Point-in-Time" join to avoid look-ahead bias. |
| **Model Optimization** | Configured LightGBM with Optuna Bayesian search and TimeSeriesSplit. | Achieved robust CV results and automated hyperparameter tuning. |
| **API Debugging** | Diagnosed 401/429 errors and identified the need for SimFin v3 mapping (GOOGL -> GOOG). | Resolved authentication issues and implemented robust error handling. |
| **UI/UX Design** | Injected custom CSS to implement a minimal aesthetic. | Created a professional, institutional-grade dashboard without standard Streamlit defaults. |
| **Trading Strategy** | Developed the backtesting simulation logic and equity curve visualization. | Provided a functional comparison between AI signals and Benchmark returns. |

## Reflections

- **What worked well:** The iterative prototyping in Jupyter Notebooks followed by automated scripting allowed for rapid testing of financial indicators.
- **Challenges:** Authentication with the SimFin API required multiple diagnostic rounds due to subtle documentation discrepancies regarding header formats.
- **Learning:** Using AI for high-volume tasks like calculating technical indicators in Polars significantly reduced boilerplate code while maintaining high efficiency.

---
*Generated as part of the project deliverables.*

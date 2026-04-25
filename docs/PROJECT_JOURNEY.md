# Project Journey: Crypto ML Predictor Decision Log

This document tracks the technical evolution, architectural decisions, and scientific insights gained during the development of the Crypto ML Predictor.

---

## Phase 1: Environment Setup and GCP Connectivity (Issue #1)
**Objective:** Establish a secure and reproducible foundation for data ingestion.

### Technologies Used
*   **Python (dotenv):** For secure environment variable management.
*   **Google Cloud BigQuery Client:** Official SDK for low-latency data extraction from the Gold dataset.
*   **Medallion Architecture:** Data source strategy using high-fidelity refined data.

### Why these choices?
*   **Security:** Using `.env` and `auth/` directory ensures service account keys are never exposed in version control (enforced via `.gitignore`).
*   **Scalability:** The `BigQueryConnector` class was designed as a singleton-ready module, allowing any part of the application to pull data without re-authenticating.

### Conclusions
*   The connection to the `analytics_data_gold` dataset is stable.
*   The schema uses `ds` as the primary time-series key and `id` as the asset identifier.

---

## Phase 2: Statistical Validation (Issue #3)
**Objective:** Prove the "Volume Shock" hypothesis before investing in model development.

### Technologies Used
*   **Pandas & Scipy (Spearman Rank):** For non-linear correlation analysis.
*   **Jupyter Notebooks:** Used strictly for Exploratory Data Analysis (EDA).
*   **Z-Score Normalization:** To standardize volume across different market caps.

### Why these choices?
*   **Spearman vs Pearson:** We chose Spearman because crypto markets are non-linear; it captures the *rank* relationship rather than just the linear distance.
*   **Dual-Horizon Analysis:** We tested T+1, T+7, and T+30 to find where the signal "matures".

### Conclusions (The "Alpha" Discovery)
*   **The 30-Day Rule:** The strongest signal found was `zscore_30d` vs `return_t30` for Bitcoin (**p-value: 0.000005**).
*   **Volume as Exhaustion:** We mathematically confirmed that extreme volume spikes (>2.0 Z) act as an "Exhaustion Signal," leading to price reversals in the following 30 days.
*   **Seasonality:** Weekends (Saturdays) are the primary birthplaces of "Black Swan" shocks due to low liquidity.

---

## Phase 3: Baseline ML Model Development (Issue #5)
**Objective:** Build a functional predictive "brain" and establish an MLOps lifecycle.

### Technologies Used
*   **XGBoost:** A gradient boosting library for high-performance tabular prediction.
*   **MLflow:** For experiment tracking and model versioning.
*   **Scikit-Learn (TimeSeriesSplit):** For honest, chronological validation.

### Why these choices?
*   **MLflow:** Essential to prevent "Experiment Chaos." Every precision score and parameter is now logged in a local database.
*   **TimeSeriesSplit:** Mandatory for financial data. It ensures we never "leak" future data into the past during training.

## Architectural Philosophy: Classification vs. Forecasting
A strategic decision was made to treat this as a **Binary Classification** problem rather than a traditional Regression/Forecasting problem.

### 1. Decision Rationale
*   **Forecasting (Regression):** Predicting the exact price of Bitcoin (e.g., $102,450.50) is highly unstable due to market noise and high-frequency volatility.
*   **Classification (Our Choice):** Predicting the **probability of a significant event** (e.g., "Price Rise > 5% in 30 days") is more robust. It filters out the noise and focuses on actionable market signals.

### 2. Time-Series ML Approach
Although we use tabular models like XGBoost, the problem remains a "Time-Series Problem" because:
*   **No Random Shuffling:** We strictly follow the arrow of time during cross-validation.
*   **Temporal Memory:** Our features (Z-Scores, Rolling Correlations) act as "Lags," providing the model with a 30-day historical context for every prediction.

---

## Conclusions

*   **Model Sensitivity:** The baseline achieved a peak precision of **0.60** in specific regimes but dropped in others. 
*   **The Context Gap:** Volume alone is not enough for a production-grade model. The model needs to understand "Market Regimes" (Bull/Bear) to interpret if a shock is a buy or sell signal.

---

## Current State & Next Steps
We are currently transitioning from **Exploration** to **Refactoring**. The "Volume Shock" signal is validated, the infrastructure is ready, and we are prepared to integrate **Volatility** and **Bitcoin Dominance** to stabilize model performance.

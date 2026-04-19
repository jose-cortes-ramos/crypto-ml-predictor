# Crypto ML Predictor: Volume-Based Price Forecasting

A production-grade Machine Learning system designed to validate and forecast cryptocurrency price movements by analyzing unusual volume patterns (Volume Shocks). This project integrates a GCP-based Medallion architecture with MLOps best practices.

---

## Technical Architecture
The system consumes processed data from the `analytics_data_gold` dataset in BigQuery, implementing a decoupled feature engineering and model training lifecycle.

*   **Ingestion:** Python-to-BigQuery connector with IAM security.
*   **Validation:** Spearman correlation analysis for volume-price hypothesis testing.
*   **Modeling:** Gradient Boosting (XGBoost) with time-series nested cross-validation.
*   **Observability:** Experiment tracking via MLflow and DVC for data versioning.

---

## Key Features
*   **Volume Z-Score Analysis:** Identifies anomalies relative to 30-day moving windows.
*   **Strict Time-Series Validation:** Prevents look-ahead bias using TimeSeriesSplit.
*   **Modular Pipeline:** Seamlessly transition from exploratory notebooks to production .py modules.
*   **Hypothesis-Driven Engineering:** Focused on statistically significant technical signals (RSI, Momentum, Lags).

---

## Tech Stack
*   **Engine:** Python (Scikit-learn, XGBoost, Pandas)
*   **Data Warehouse:** Google Cloud BigQuery
*   **MLOps:** MLflow, Great Expectations
*   **Infrastructure:** GCP IAM, BigQuery API

---

## Project Structure
```text
├── docs/               # Architecture and master plans
├── notebooks/          # Exploratory Data Analysis (EDA)
├── src/                # Production-ready modules
│   ├── features/       # Feature engineering factory
│   └── models/         # Model training and inference
├── tests/              # Unit and integration tests
└── requirements.txt    # Project dependencies
```

---

## Getting Started
1. Clone the repository.
2. Configure .env with GCP credentials and Project ID.
3. Install dependencies: pip install -r requirements.txt
4. Execute the EDA notebook: jupyter notebook notebooks/01_eda_validation.ipynb

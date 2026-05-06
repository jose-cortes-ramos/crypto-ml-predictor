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

## Usage & Deployment
To generate real-time market signals based on the latest BigQuery data:

1. **Configure Environment:** Ensure your `.env` file is set and `auth/credentials.json` is present.
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run Inference:**
   ```bash
   python src/models/predict.py
   ```

## Development Workflow
- **Validation:** Use `notebooks/01_eda_validation.ipynb` for hypothesis testing.
- **MLOps:** Training history is logged in `mlruns/`. Use `mlflow ui` to compare experiment performance.

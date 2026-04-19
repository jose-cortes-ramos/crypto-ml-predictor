# GitHub Technical Issues: Crypto ML Predictor

Detailed technical tasks and engineering notes for project execution. These entries are intended for synchronization with GitHub Issues.

---

## Issue 1: Environment Setup and GCP Connectivity
- **Description:** Initialize the project environment and establish secure connectivity with BigQuery.
- **Engineering Tasks:**
    1.  Create `requirements.txt` with essential ML libraries (Pandas, Scikit-Learn, XGBoost, MLflow).
    2.  Set up `.env` for GCP credentials and project IDs.
    3.  Implement a base data extraction script using the Google Cloud BigQuery client.
- **Notes:** Must follow the principle of least privilege for IAM roles.

## Issue 2: Statistical Validation of Volume Shock Hypothesis
- **Description:** Execute a quantitative analysis to validate the correlation between volume spikes and price returns.
- **Engineering Tasks:**
    1.  Initialize `notebooks/01_eda_validation.ipynb` for visual and statistical analysis.
    2.  Calculate Volume Z-Score with a 30-day moving window.
    3.  Compute Spearman correlation coefficients for Volume Shock at T versus Return at T+1.
- **Notes:** Perform analysis across multiple crypto assets to ensure generalizability.

## Issue 3: Feature Engineering and Baseline Model Implementation
- **Description:** Develop the initial predictive model using technical indicators and temporal lags.
- **Engineering Tasks:**
    1.  Implement feature generation for Lags (1, 3, 7 days), RSI, and Momentum.
    2.  Configure Time-Series Nested Cross-Validation for model training.
    3.  Train a baseline XGBoost classifier and register parameters in MLflow.
- **Notes:** Avoid look-ahead bias by ensuring strictly temporal data splits.

## Issue 4: Refactor to Production Modules
- **Description:** Transition exploratory code into modular, production-grade Python scripts.
- **Engineering Tasks:**
    1.  Migrate feature logic to `src/features/feature_factory.py`.
    2.  Implement model training pipeline in `src/models/trainer.py`.
    3.  Integrate data quality validation checks.
- **Notes:** Ensure 100% compliance with existing linting and formatting standards.

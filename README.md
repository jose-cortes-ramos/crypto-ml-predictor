# Crypto Tsunami Intelligence: Predictive Market Exhaustion System
## Part of the Data Engineering and AI Portfolio

This repository represents the Modeling and Production phase of a full-stack data ecosystem. It leverages structural market anomalies (Volume Tsunamis) to classify price reversals with institutional-grade precision.

---

## 1. Problem Statement
The primary challenge in cryptocurrency trading is the high signal-to-noise ratio during volatility spikes. Standard technical indicators often fail to distinguish between Healthy Momentum (Buying) and a Buying Climax (Exhaustion).

**The Question:** Given a structural volume shock (Z-Score > 2.0), can we classify with institutional precision if the price will rise by more than 5% in the following 30 days? 

This system transforms raw volume data into actionable binary signals (Green/Red) to eliminate emotional bias during extreme market events.

---

## 2. Exploratory Data Analysis (EDA) and Statistical Proof
Building upon the insights from the [crypto-market-analysis](https://github.com/jose-cortes-ramos/crypto-market-analysis) repository, we established a scientific foundation:

*   **Hypothesis Testing:** Used Spearman Rank Correlation to prove the non-linear relationship between volume shocks and 30-day returns.
*   **Key Discovery:** Confirmed a causal link with a p-value of 0.000005, validating that volume anomalies are statistically significant leading indicators of trend reversals.
*   **Feature Engineering:** Identified that a 30-day rolling window provides the optimal Signal Maturity for structural trend changes compared to intraday noise.

---

## 3. Model Selection and Justification
The project transitioned from exploratory baselines to a production XGBoost Classifier:

*   **Non-Linear Decision Boundaries:** Unlike linear models, XGBoost's ensemble of trees maps the complex rule that "high volume is bullish at bottoms but bearish at tops."
*   **Optimization:** We used Gradient Boosting with Taylor Expansion (2nd order derivatives) to navigate the extreme intra-day volatility of crypto markets.
*   **Robustness:** Binary classification was chosen over price forecasting (regression) to filter out daily price noise and focus on high-conviction trends.

---

## 4. Evaluation Metrics and Performance Baseline
The model is evaluated against a Naive Random Guess (50%) baseline using strict chronological Time-Series splitting.

| Metric | System Performance | Baseline (Naive) | Improvement (Lift) |
| :--- | :--- | :--- | :--- |
| Momentum Accuracy (Green) | 79.6% | 50.0% | +29.6% |
| Exhaustion Accuracy (Red) | 73.7% | 50.0% | +23.7% |

*Validated across 87 structural volume shocks (Tsunami events).*

---

## 5. Technical Limitations and Honest Boundaries
In alignment with professional standards, we acknowledge the following constraints:
*   **Sideways Markets:** The model is specialized for Shock events. In low-volatility, sideways markets, the predictive power is diminished.
*   **Capitulation Bias:** Forensic auditing identified a False Bearish bias during extreme panics (e.g., Feb 2026), where the model misinterprets high-volume capitulation as exhaustion.
*   **Data Freshness:** Predictions are tied to daily close data. Intraday volatility is not currently captured in the inference engine.

---

## Portfolio Ecosystem Narrative
This project is the predictive engine of a multi-repository architecture:
1.  **[de-crypto-pipeline](https://github.com/jose-cortes-ramos/de-crypto-pipeline):** Data ingestion, quality control, and storage.
2.  **[crypto-market-analysis](https://github.com/jose-cortes-ramos/crypto-market-analysis):** Deep EDA, visualization, and statistical discovery.
3.  **[crypto-ml-predictor](https://github.com/jose-cortes-ramos/crypto-ml-predictor):** (This Repo) Production ML modeling and cloud-scale inference.

---
Developed by Jose Cortes Ramos | Data Engineering and AI Solutions

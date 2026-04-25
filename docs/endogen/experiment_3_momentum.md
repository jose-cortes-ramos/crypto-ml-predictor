# Experiment 3: Momentum and Trend Fusion

## Objective
Attempt to stabilize the volume signal by adding structural trend indicators (Moving Averages).

## Variables Selection
*   **zscore_30d:** Primary volume anomaly signal.
*   **price_vs_ma30:** Ratio between current price and 30-day moving average (Trend indicator).
*   **price_change_7d:** Weekly price momentum.

## Rationale
Testing if "Volume Shocks" are more predictive when they align with the prevailing trend. This is a "Minimalist" approach to context, using only 3 powerful features to avoid the noise of Experiment 2.

## Results (TimeSeriesSplit Precision)
*   Fold 0: 0.1500
*   Fold 1: 0.2188
*   Fold 2: 0.3571
*   Fold 3: 0.1429
*   Fold 4: 0.4000
*   **Average: 0.2537**

## Conclusions
The Momentum model provided better stability than the Full Endogenous model (Test 2) by avoiding zero-precision folds. However, it did not outperform the raw Volume Baseline (Test 1) peak of 0.60. This suggests that while trend alignment helps, the core predictive power still resides primarily in the volume anomaly itself.

# Experiment 2: Full Endogenous Features

## Objective
Enhance the baseline by adding context variables (Volatility, Dominance, and Divergence).

## Variables Selection
*   **zscore_30d:** Volume anomaly.
*   **volatility_30d:** Standard deviation of daily returns.
*   **price_vol_corr:** Rolling correlation between price and volume.
*   **market_cap_dominance:** Asset weight in the global crypto market.
*   **day_of_week:** Calendar seasonality.

## Rationale
Hypothesized that the model needed "Market Context" to interpret if a volume shock was a buying climax or a panic sell.

## Results (TimeSeriesSplit Precision)
*   Fold 0: 0.0000
*   Fold 1: 0.0000
*   Fold 2: 0.0600
*   Fold 3: 0.2718
*   Fold 4: 0.0888
*   **Average:** 0.0841

## Conclusions
**Failure Analysis:** Adding too many non-linear variables to a small dataset (1685 rows) resulted in high bias and poor generalization. The model became overly conservative (returning 0.00 precision in early folds).

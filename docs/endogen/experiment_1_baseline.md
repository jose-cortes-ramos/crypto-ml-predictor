# Experiment 1: Baseline Volume Shock

## Objective
Establish a performance floor using only the primary hypothesis: unusual volume spikes as a predictor of price reversals.

## Variables Selection
*   **zscore_30d (Independent):** Standardized volume anomaly relative to a 30-day rolling window.
*   **return_t30 (Target):** Binary classification of price rise > 5% in the following 30 days.

## Rationale
Identify if volume alone contains enough "Alpha" to justify more complex modeling. Standardized Z-Score allows the model to compare assets of different sizes (BTC vs SOL).

## Results (TimeSeriesSplit Precision)
*   Fold 0: 0.1364
*   Fold 1: 0.2941
*   **Fold 2: 0.6000 (Peak Performance)**
*   Fold 3: 0.2667
*   Fold 4: 0.3333
*   **Average:** 0.3261

## Conclusions
The volume signal has significant predictive power in specific market regimes (Fold 2), but lacks stability across the entire timeline.

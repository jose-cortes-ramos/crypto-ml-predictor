# Looker Studio Visualization Strategy: Crypto Intelligence Dashboard

This document outlines the step-by-step construction of the visual intelligence layer, integrating the GCP Data Hub with the Machine Learning inference results.

---

## 1. Dashboard UX/UI Principles
To maintain high-tier fintech standards (Airbnb/AWS style), the dashboard must follow these guidelines:
*   **Minimalist Cognitive Load:** Maximum of 3 charts per row.
*   **Color Palette:** Dark Mode First. Use Teal (#008080) for Bullish signals and Coral (#FF7F50) for Bearish/Risk signals.
*   **Interactivity:** Global filters for `Asset ID` and `Date Range` must be present on every page.

---

## 2. Recommended Historical Charts

### Chart 1: Price and ML Signal Convergence
*   **Type:** Line Chart with Scatter Overlay.
*   **Metrics:** `price` (Line), `ml_prediction` (Points/Markers).
*   **Dimension:** `ds` (Time).
*   **Purpose:** Visualize if the model successfully predicted price drops/rises. Highlight the October 2025 crash with the ML signal.

### Chart 2: The Pulse (Volume Z-Score vs. Volatility)
*   **Type:** Combined Area and Line Chart.
*   **Metrics:** `zscore_30d` (Area), `volatility_30d` (Line).
*   **Purpose:** Identify "Volume Shocks" as the leading indicator of market nervousness. Any Z-Score area above 2.0 indicates a high-risk zone.

### Chart 3: Confidence Distribution Matrix
*   **Type:** Bubble Chart (Scatter Plot).
*   **X-Axis:** `zscore_30d`.
*   **Y-Axis:** `ml_probability`.
*   **Bubble Size:** `total_volume`.
*   **Purpose:** Filter the "noise." Large bubbles in high probability/high Z-score quadrants are the institutional "Smart Money" signals.

### Chart 4: Seasonality Performance (Day of Week)
*   **Type:** Treemap or Bar Chart.
*   **Dimension:** `day_name`.
*   **Metric:** `Average return_t30`.
*   **Purpose:** Confirm the "Wednesday Exhaustion" and "Thursday Momentum" findings discovered during the statistical validation phase.

---

## 3. Step-by-Step Implementation Guide

### Step 1: Data Connection
1.  Open Looker Studio.
2.  Create a new Data Source using the **BigQuery Connector**.
3.  Select the project `gcp-data-plataform-hub` and the dataset `analytics_data_gold`.
4.  Use the SQL Join provided in `LOOKER_INTEGRATION.md` to merge trends with ML predictions.

### Step 2: Key Performance Indicators (KPIs)
Add 3 Scorecards at the top of the dashboard:
1.  **Current Price:** Last available price for the selected asset.
2.  **Market Pulse:** Latest `zscore_30d` value.
3.  **Model Confidence:** Latest `ml_probability` percentage.

### Step 3: Predictive Alerts
Use **Conditional Formatting** on the Price Signal Chart:
*   If `ml_prediction = 1` ➔ Marker Color = Teal.
*   If `ml_prediction = 0` ➔ Marker Color = Coral.

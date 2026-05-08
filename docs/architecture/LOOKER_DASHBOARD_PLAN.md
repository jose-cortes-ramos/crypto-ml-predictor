# Looker Studio Dashboard Implementation Plan

This document defines the final layout and component configuration for the Crypto ML Predictor dashboard.

---

## 1. Top KPI Layer (Scorecards)
- **Asset Selector:** Dropdown for coin identification (BTC, ETH, etc.).
- **Live Price:** Current market value.
- **Market Pulse:** Latest Volume Z-Score.
- **Model Confidence:** Latest ML Probability.

## 2. Temporal Intelligence (Main View)
- **Chart A (Price Overlay):** Time series chart with price line and ML markers.
- **Chart B (Volume Pulse):** Area chart showing structural shocks (Z-Score > 2.0 highlighted).
- **Alignment:** Charts A and B must share the same X-axis (Timeline) for causality analysis.

## 3. Forensic Analysis (Bottom View)
- **Seasonality Bar Chart:** Average 30-day return grouped by day of the week.
- **Tsunami Table:** Drill-down list of the 10 most extreme historical events.
- **Fields:** Date, Initial Price, Z-Score, Prediction, Confidence, 30d Result.

---

## 4. Branding & UX
- **Theme:** Dark Mode (Institutional High-Contrast).
- **Interaction:** Cross-filtering enabled (clicking a Tsunami in the table highlights it on the chart).

import os
import sys

# Senior Architect Fix
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pandas as pd
import numpy as np
import mlflow
import mlflow.xgboost
from datetime import datetime, timezone
from src.data.bq_connector import BigQueryConnector
from src.features.feature_factory import FeatureFactory

def get_most_stable_model(experiment_name="crypto-momentum-xgboost"):
    """Selects the best model in the experiment based on stability."""
    print(f"[+] Analyzing model stability in experiment: {experiment_name}")
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if not experiment:
        experiment = mlflow.get_experiment_by_name("crypto-production-xgboost")
        if not experiment:
            raise Exception("No valid experiments found in MLflow.")

    runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id])
    if runs.empty:
        raise Exception("No runs found.")

    precision_cols = [c for c in runs.columns if 'metrics.precision_fold_' in c]
    if not precision_cols:
        return f"runs:/{runs.iloc[0].run_id}/production_model"
        
    runs['mean_precision'] = runs[precision_cols].mean(axis=1)
    runs['std_precision'] = runs[precision_cols].std(axis=1).fillna(0)
    runs['stability_score'] = runs['mean_precision'] - runs['std_precision']

    best_run = runs.sort_values('stability_score', ascending=False).iloc[0]
    
    print(f"[SUCCESS] Winner Run ID: {best_run.run_id} (Avg: {best_run.mean_precision:.2%})")
    
    artifact_name = "momentum_model_v3" if "momentum" in experiment.name else "production_model"
    return f"runs:/{best_run.run_id}/{artifact_name}"

def predict_today():
    print("[+] Initializing Dynamic Inference Engine...")
    try:
        # 1. Data Ingestion
        connector = BigQueryConnector()
        df = connector.fetch_historical_trends()
        df['ds'] = pd.to_datetime(df['ds'])
        
        # CRITICAL FIX: Ensure ascending order for rolling window calculations
        df = df.sort_values(['id', 'ds'], ascending=True).reset_index(drop=True)
        
        # 2. Feature Generation
        df = FeatureFactory.create_features(df)
        
        # 3. Select Features
        features_v3 = ['zscore_30d', 'price_vs_ma30', 'price_change_7d']
        
        # Get the latest row for each asset after features are calculated
        latest_data = df.groupby('id').tail(1).copy()
        
        # Check if we still have NaNs
        if latest_data[features_v3].isnull().values.any():
            print("[WARNING] Some features are still NaN. Check if BigQuery has enough history (min 30 days).")
        
        X = latest_data[features_v3]

        # 4. Load & Predict
        model_uri = get_most_stable_model()
        model = mlflow.xgboost.load_model(model_uri)
        
        latest_data['prediction'] = model.predict(X)
        latest_data['probability'] = model.predict_proba(X)[:, 1]
        
        print("\n" + "="*50)
        print(" CRYPTO ML PREDICTOR: LIVE SIGNALS ")
        print("="*50)
        for _, row in latest_data.iterrows():
            signal = "BULLISH (BUY)" if row['prediction'] == 1 else "BEARISH/STABLE (WAIT)"
            print(f"Asset: {row['id'].upper()}")
            print(f"Signal: {signal}")
            print(f"Confidence: {row['probability']:.2%}")
            print(f"Metrics: Z30={row['zscore_30d']:.2f}, Trend={row['price_vs_ma30']:.2f}")
            print("-" * 20)
        print("="*50 + "\n")

    except Exception as e:
        print(f"[ERROR] Inference failed: {e}")

if __name__ == "__main__":
    predict_today()

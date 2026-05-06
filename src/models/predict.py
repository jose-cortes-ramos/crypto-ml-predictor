import os
import sys

# Senior Architect Fix
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pandas as pd
import mlflow.xgboost
from src.data.bq_connector import BigQueryConnector
from src.features.feature_factory import FeatureFactory
from src.utils.mlflow_utils import get_most_stable_model

def predict_today():
    print("[+] Initializing Dynamic Inference Engine...")
    try:
        connector = BigQueryConnector()
        df = connector.fetch_historical_trends()
        df['ds'] = pd.to_datetime(df['ds'])
        df = df.sort_values(['id', 'ds'], ascending=True).reset_index(drop=True)
        
        df = FeatureFactory.create_features(df)
        features_v3 = ['zscore_30d', 'price_vs_ma30', 'price_change_7d']
        latest_data = df.groupby('id').tail(1).copy()
        X = latest_data[features_v3]

        model_uri = get_most_stable_model()
        model = mlflow.xgboost.load_model(model_uri)
        
        latest_data['prediction'] = model.predict(X)
        latest_data['probability'] = model.predict_proba(X)[:, 1]
        
        print("\n" + "="*50)
        print(" CRYPTO ML PREDICTOR: LIVE SIGNALS ")
        print("="*50)
        for _, row in latest_data.iterrows():
            signal = "BULLISH" if row['prediction'] == 1 else "BEARISH/STABLE"
            print(f"Asset: {row['id'].upper()} | Signal: {signal} | Confidence: {row['probability']:.2%}")
        print("="*50 + "\n")

    except Exception as e:
        print(f"[ERROR] Inference failed: {e}")

if __name__ == "__main__":
    predict_today()

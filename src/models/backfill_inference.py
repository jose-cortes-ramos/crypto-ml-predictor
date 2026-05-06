import os
import sys
import pandas as pd
import mlflow.xgboost

# Fix path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.data.bq_connector import BigQueryConnector
from src.features.feature_factory import FeatureFactory
from src.utils.mlflow_utils import get_most_stable_model

def run_looker_backfill():
    print("="*50)
    print(" STARTING LOOKER ML ENRICHMENT (DYNAMIC MODE) ")
    print("="*50)
    
    try:
        # 1. Fetch
        connector = BigQueryConnector()
        df = connector.fetch_historical_trends()
        df['ds'] = pd.to_datetime(df['ds'])
        df = df.sort_values(['id', 'ds'], ascending=True).reset_index(drop=True)
        
        # 2. Features
        df = FeatureFactory.create_features(df)
        df = df.dropna(subset=['zscore_30d', 'price_vs_ma30'])
        
        # 3. Dynamic Model Loading (NO HARDCODING)
        model_uri = get_most_stable_model()
        model = mlflow.xgboost.load_model(model_uri)
        
        # 4. Predict
        features = ['zscore_30d', 'price_vs_ma30', 'price_change_7d']
        X = df[features]
        print(f"[+] Running dynamic inference on {len(df)} records...")
        df['ml_prediction'] = model.predict(X)
        df['ml_probability'] = model.predict_proba(X)[:, 1]
        
        # 5. Load to BigQuery
        looker_columns = ['id', 'ds', 'zscore_30d', 'price_vs_ma30', 'ml_prediction', 'ml_probability']
        connector.write_predictions(df[looker_columns], table_name="crypto_ml_predictions")
        
        print("\n" + "="*50)
        print(" [SUCCESS] DYNAMIC BACKFILL COMPLETE ")
        print("="*50)

    except Exception as e:
        print(f"\n[ERROR] Backfill failed: {e}")

if __name__ == "__main__":
    run_looker_backfill()

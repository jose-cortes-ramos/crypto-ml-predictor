import os
import sys
import pandas as pd
import mlflow.xgboost
from src.data.bq_connector import BigQueryConnector
from src.features.feature_factory import FeatureFactory

# Add root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

def predict_today():
    """
    Production inference script.
    Loads the latest model and predicts market regime for the current data.
    """
    print("[+] Fetching latest market data...")
    connector = BigQueryConnector()
    df = connector.fetch_historical_trends()
    df['ds'] = pd.to_datetime(df['ds'])
    
    # 1. Feature Engineering
    df = FeatureFactory.create_features(df)
    
    # Get the latest data point for inference
    latest_data = df.sort_values('ds').groupby('id').tail(1)
    features = ['zscore_30d', 'price_vol_corr', 'volatility_30d', 'market_cap_dominance', 'day_of_week']
    X = latest_data[features]
    
    # 2. Load Model from MLflow
    # Note: Using the model logged in the training run
    model_uri = "runs:/d19562ae28bc4154941b488f51b3a5c9/enhanced_model_v2" # Reemplazar con el Run ID real de MLflow
    print("[+] Loading model from MLflow...")
    try:
        model = mlflow.xgboost.load_model(model_uri)
        
        # 3. Predict
        latest_data['prediction'] = model.predict(X)
        latest_data['probability'] = model.predict_proba(X)[:, 1]
        
        print("\n--- Market Signals for Today ---")
        print(latest_data[['id', 'ds', 'prediction', 'probability']])
        
    except Exception as e:
        print(f"[ERROR] Could not load model: {e}")

if __name__ == "__main__":
    predict_today()

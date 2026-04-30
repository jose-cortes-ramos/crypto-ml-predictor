import os
import sys
import pandas as pd
import mlflow
import mlflow.xgboost
from xgboost import XGBClassifier
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import classification_report

# Senior Architect Fix: Ensure root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.data.bq_connector import BigQueryConnector
from src.features.feature_factory import FeatureFactory

def train_production_model():
    """
    Refactored training pipeline using FeatureFactory.
    Ensures consistency between training and future inference.
    """
    print("[+] Fetching data from BigQuery...")
    connector = BigQueryConnector()
    df = connector.fetch_historical_trends()
    df['ds'] = pd.to_datetime(df['ds'])
    df = df.sort_values(['id', 'ds'])

    print("[+] Applying features via FeatureFactory...")
    df = FeatureFactory.create_features(df)
    
    # Define Target
    df['target'] = (df.groupby('id')['price'].pct_change(30).shift(-30) > 0.05).astype(int)
    df = df.dropna()

    features = ['zscore_30d', 'price_vol_corr', 'volatility_30d', 'day_of_week', 'is_month_end']
    X = df[features]
    y = df['target']

    # MLOps: Experiment Tracking
    mlflow.set_experiment("crypto-production-xgboost")
    
    with mlflow.start_run(run_name="Production_Baseline_Refactored"):
        tscv = TimeSeriesSplit(n_splits=5)
        
        for fold, (train_index, test_index) in enumerate(tscv.split(X)):
            X_train, X_test = X.iloc[train_index], X.iloc[test_index]
            y_train, y_test = y.iloc[train_index], y.iloc[test_index]

            model = XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=4, random_state=42)
            model.fit(X_train, y_train)

            precision = classification_report(y_test, model.predict(X_test), output_dict=True)['1']['precision']
            mlflow.log_metric(f"precision_fold_{fold}", precision)
            print(f"Fold {fold} precision: {precision:.4f}")

        # Final storage
        model.fit(X, y)
        mlflow.xgboost.log_model(model, "production_model")
        print("[SUCCESS] Production model refactored and logged.")

if __name__ == "__main__":
    train_production_model()

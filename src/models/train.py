import os
import sys

# Senior Architect Fix: Ensure root is in path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pandas as pd
import mlflow
import mlflow.xgboost
from xgboost import XGBClassifier
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import classification_report
from src.data.bq_connector import BigQueryConnector

def train_baseline_model():
    # 1. Ingestion
    print("[+] Fetching data from BigQuery...")
    connector = BigQueryConnector()
    df = connector.fetch_historical_trends()
    df['ds'] = pd.to_datetime(df['ds'])
    df = df.sort_values(['id', 'ds'])

    # 2. Feature Engineering (Baseline)
    df['zscore_30d'] = df.groupby('id', group_keys=False).apply(
        lambda x: (x['total_volume'] - x['total_volume'].rolling(30).mean()) / x['total_volume'].rolling(30).std()
    )
    df['target'] = (df.groupby('id')['price'].pct_change(30).shift(-30) > 0.05).astype(int)
    df = df.dropna()

    features = ['zscore_30d']
    X = df[features]
    y = df['target']

    # 3. MLOps: Experiment Tracking
    mlflow.set_experiment("crypto-baseline-xgboost")
    
    with mlflow.start_run():
        # Time-Series Split (Ensures we never train on future data)
        tscv = TimeSeriesSplit(n_splits=5)
        
        for fold, (train_index, test_index) in enumerate(tscv.split(X)):
            X_train, X_test = X.iloc[train_index], X.iloc[test_index]
            y_train, y_test = y.iloc[train_index], y.iloc[test_index]

            model = XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=3)
            model.fit(X_train, y_train)

            # Evaluation
            preds = model.predict(X_test)
            report = classification_report(y_test, preds, output_dict=True)
            
            # Log metrics to MLflow
            mlflow.log_metric(f"precision_fold_{fold}", report['1']['precision'])
            print(f"Fold {fold} precision: {report['1']['precision']:.4f}")

        # Final training and saving
        model.fit(X, y)
        mlflow.xgboost.log_model(model, "model")
        print("[SUCCESS] Baseline model trained and logged to MLflow.")

if __name__ == "__main__":
    train_baseline_model()

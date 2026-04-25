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

def train_momentum_model():
    """
    TEST 3: MOMENTUM & TREND MODEL
    Goal: Combine Volume Shocks with Price Trends (MA30) and Weekly Momentum.
    """
    print("[+] TEST 3: Fetching data from BigQuery...")
    connector = BigQueryConnector()
    df = connector.fetch_historical_trends()
    df['ds'] = pd.to_datetime(df['ds'])
    df = df.sort_values(['id', 'ds'])

    print("[+] TEST 3: Computing Momentum & Trend features...")
    
    # 1. Volume Signal (The Core)
    df['zscore_30d'] = df.groupby('id', group_keys=False).apply(
        lambda x: (x['total_volume'] - x['total_volume'].rolling(30).mean()) / x['total_volume'].rolling(30).std()
    )
    
    # 2. Trend Signal (Price vs Media Móvil 30d)
    # Ratio > 1 means price is above the monthly trend
    df['ma30'] = df.groupby('id')['price'].transform(lambda x: x.rolling(30).mean())
    df['price_vs_ma30'] = df['price'] / df['ma30']
    
    # 3. Momentum Signal (Weekly Change)
    # How much did the price change in the last 7 days?
    df['price_change_7d'] = df.groupby('id')['price'].pct_change(7)

    # Target: Price Rise > 5% in 30 days
    df['target'] = (df.groupby('id')['price'].pct_change(30).shift(-30) > 0.05).astype(int)
    
    df = df.dropna()

    features = ['zscore_30d', 'price_vs_ma30', 'price_change_7d']
    X = df[features]
    y = df['target']

    # MLOps: Experiment Tracking
    mlflow.set_experiment("crypto-momentum-xgboost")
    
    with mlflow.start_run(run_name="Momentum_Trend_V3"):
        mlflow.log_params({
            "version": "v3",
            "feature_set": "volume_z30_ma30_mom7d",
            "model": "XGBoost"
        })
        
        tscv = TimeSeriesSplit(n_splits=5)
        print(f"[+] Starting TimeSeriesSplit on {len(df)} records...")
        
        for fold, (train_index, test_index) in enumerate(tscv.split(X)):
            X_train, X_test = X.iloc[train_index], X.iloc[test_index]
            y_train, y_test = y.iloc[train_index], y.iloc[test_index]

            model = XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
            model.fit(X_train, y_train)

            preds = model.predict(X_test)
            report = classification_report(y_test, preds, output_dict=True, zero_division=0)
            
            precision = report['1']['precision']
            mlflow.log_metric(f"precision_fold_{fold}", precision)
            print(f"Fold {fold} precision: {precision:.4f}")

        # Final storage
        model.fit(X, y)
        mlflow.xgboost.log_model(model, "momentum_model_v3")
        print("[SUCCESS] Momentum model V3 trained and logged to MLflow.")

if __name__ == "__main__":
    train_momentum_model()

import os
import sys
import pandas as pd
import mlflow
import mlflow.xgboost
from xgboost import XGBClassifier
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import classification_report

# Senior Architect Fix: Ensure root is in path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.data.bq_connector import BigQueryConnector

def train_enhanced_model():
    """
    TEST 2: ENHANCED ENDOGENOUS MODEL
    Goal: Improve baseline by adding Volatility, Divergence, and Calendar features.
    """
    print("[+] TEST 2: Fetching data from BigQuery...")
    connector = BigQueryConnector()
    df = connector.fetch_historical_trends()
    df['ds'] = pd.to_datetime(df['ds'])
    df = df.sort_values(['id', 'ds'])

    print("[+] TEST 2: Computing enhanced features (Context + Structure)...")
    
    # Feature 1: Volume Shock (Validated in Test 1)
    df['zscore_30d'] = df.groupby('id', group_keys=False).apply(
        lambda x: (x['total_volume'] - x['total_volume'].rolling(30).mean()) / x['total_volume'].rolling(30).std()
    )
    
    # Feature 2: Volatility (The 'Panic' sensor)
    df['volatility_30d'] = df.groupby('id')['daily_variation'].rolling(30).std().reset_index(0, drop=True)
    
    # Feature 3: Price-Volume Correlation (The 'Trend Health' sensor)
    df['price_vol_corr'] = df.groupby('id', group_keys=False).apply(
        lambda x: x['price'].rolling(30).corr(x['total_volume'])
    )
    
    # Feature 4: Market Cap Dominance (The 'Macro Crypto' sensor)
    # market_cap_dominance is already in the Gold table

    # Feature 5: Calendar (The 'Institutional' sensor)
    df['day_of_week'] = df['ds'].dt.dayofweek

    # Target: Price Rise > 5% in 30 days
    df['target'] = (df.groupby('id')['price'].pct_change(30).shift(-30) > 0.05).astype(int)
    
    df = df.dropna()

    features = ['zscore_30d', 'volatility_30d', 'price_vol_corr', 'market_cap_dominance', 'day_of_week']
    X = df[features]
    y = df['target']

    # MLOps: Experiment Tracking
    mlflow.set_experiment("crypto-enhanced-xgboost")
    
    with mlflow.start_run(run_name="Enhanced_Endogenous_V2"):
        # Log which features we are using in this version
        mlflow.log_param("version", "v2")
        mlflow.log_param("feature_set", "volumen_volatilidad_calendario_dominancia")
        
        tscv = TimeSeriesSplit(n_splits=5)
        print(f"[+] Starting TimeSeriesSplit on {len(df)} records...")
        
        for fold, (train_index, test_index) in enumerate(tscv.split(X)):
            X_train, X_test = X.iloc[train_index], X.iloc[test_index]
            y_train, y_test = y.iloc[train_index], y.iloc[test_index]

            # We increase max_depth slightly as we have more context now
            model = XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=4, random_state=42)
            model.fit(X_train, y_train)

            preds = model.predict(X_test)
            report = classification_report(y_test, preds, output_dict=True, zero_division=0)
            
            precision = report['1']['precision']
            mlflow.log_metric(f"precision_fold_{fold}", precision)
            print(f"Fold {fold} precision: {precision:.4f}")

        # Final model storage
        model.fit(X, y)
        mlflow.xgboost.log_model(model, "enhanced_model_v2")
        print("[SUCCESS] Enhanced model V2 trained and logged to MLflow.")

if __name__ == "__main__":
    train_enhanced_model()

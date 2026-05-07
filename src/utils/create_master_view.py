import os
from google.cloud import bigquery
from dotenv import load_dotenv

# Absolute path configuration
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
load_dotenv(os.path.join(ROOT_DIR, '.env'))

def create_master_view():
    """
    Creates the final unified view for Looker Studio.
    Includes future returns for historical impact analysis.
    """
    project_id = os.getenv('GCP_PROJECT_ID')
    dataset_id = os.getenv('GCP_DATASET_ID')
    client = bigquery.Client(project=project_id)
    
    view_id = f"{project_id}.{dataset_id}.vw_looker_master_intelligence"
    
    sql = f"""
    SELECT 
        t.id,
        t.ds,
        t.price,
        t.total_volume,
        t.market_cap_dominance,
        -- ML Intelligence Layer
        p.zscore_30d as ml_volume_zscore,
        p.price_vs_ma30 as ml_trend_ratio,
        p.ml_prediction,
        p.ml_probability,
        -- Historical Impact (The 'Future' Reality for backtesting visuals)
        -- We calculate the 30-day return using LEAD window function
        (LEAD(t.price, 30) OVER(PARTITION BY t.id ORDER BY t.ds ASC) - t.price) / t.price as return_t30
    FROM 
        `{project_id}.{dataset_id}.crypto_historical_trends` as t
    LEFT JOIN 
        `{project_id}.{dataset_id}.crypto_ml_predictions` as p
        ON t.id = p.id AND t.ds = p.ds
    """
    
    view = bigquery.Table(view_id)
    view.view_query = sql
    
    print(f"REPORT: Updating Master View at {view_id}")
    try:
        client.delete_table(view_id, not_found_ok=True)
        client.create_table(view)
        print("RESULT: SUCCESS. View now includes return_t30.")
    except Exception as e:
        print(f"RESULT: ERROR. View update failed: {e}")

if __name__ == "__main__":
    create_master_view()

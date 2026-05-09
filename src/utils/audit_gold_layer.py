import os
from google.cloud import bigquery
from dotenv import load_dotenv
import pandas as pd

# Setup paths
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
load_dotenv(os.path.join(ROOT_DIR, '.env'))

def audit_gold_layer():
    """
    Audits the Full Gold Layer ecosystem.
    Trends -> Analytics -> ML -> Master View
    """
    project_id = os.getenv('GCP_PROJECT_ID')
    dataset_id = os.getenv('GCP_DATASET_ID')
    client = bigquery.Client(project=project_id)
    
    entities = {
        "1. TRENDS (Raw Gold)": f"{project_id}.{dataset_id}.crypto_historical_trends",
        "2. ANALYTICS (Refined)": f"{project_id}.{dataset_id}.crypto_historical_analytics",
        "3. ML (Intelligence)": f"{project_id}.{dataset_id}.crypto_ml_predictions",
        "4. MASTER VIEW (Looker)": f"{project_id}.{dataset_id}.vw_looker_master_intelligence"
    }
    
    print(f"\n{'='*80}")
    print(f"FULL GOLD LAYER AUDIT - DATE: 2026-05-08")
    print(f"{'='*80}\n")
    
    for label, entity_id in entities.items():
        print(f"🔍 AUDITING {label}...")
        try:
            table = client.get_table(entity_id)
            
            # Row count
            count_query = f"SELECT COUNT(*) as total FROM `{entity_id}`"
            count_res = client.query(count_query).to_dataframe()
            total_rows = count_res['total'][0]
            
            # Last modified
            last_mod = table.modified.strftime('%Y-%m-%d %H:%M:%S')
            
            print(f"   - Row Count: {total_rows:,}")
            print(f"   - Last Updated: {last_mod}")
            print(f"   - Schema Architecture:")
            
            schema_info = []
            for field in table.schema:
                schema_info.append({"Field": field.name, "Type": field.field_type})
            print(pd.DataFrame(schema_info).to_string(index=False))
            print(f"\n{'-'*80}\n")
            
        except Exception as e:
            print(f"   - [MISSING/ERROR] Could not find {label}: {e}\n")

if __name__ == "__main__":
    audit_gold_layer()

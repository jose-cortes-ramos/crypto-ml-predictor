import os
import glob
from google.cloud import bigquery
from dotenv import load_dotenv

# Absolute path configuration
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
load_dotenv(os.path.join(ROOT_DIR, '.env'))

def deploy_views():
    """
    Deploys BigQuery views in the correct dependency order.
    1. Base Master View
    2. Specialized Analytics Views
    """
    project_id = os.getenv('GCP_PROJECT_ID')
    dataset_id = os.getenv('GCP_DATASET_ID')
    client = bigquery.Client(project=project_id)
    
    views_dir = os.path.join(ROOT_DIR, 'infra/bigquery/views')
    
    # Priority 1: The engine (Master View)
    master_view_file = os.path.join(views_dir, 'vw_looker_master_intelligence.sql')
    # Priority 2: The wheels (Rest of the views)
    other_view_files = [f for f in glob.glob(f"{views_dir}/*.sql") if 'vw_looker_master_intelligence' not in f]

    deployment_order = [master_view_file] + sorted(other_view_files)

    print(f"\n[START] AUTOMATED INFRASTRUCTURE DEPLOYMENT [{project_id}]")
    print("=" * 70)

    for file_path in deployment_order:
        if not os.path.exists(file_path):
            continue
            
        view_name = os.path.basename(file_path).replace('.sql', '')
        
        with open(file_path, 'r') as f:
            sql_content = f.read()
            
        sql_content = sql_content.replace('{{PROJECT_ID}}', project_id)
        sql_content = sql_content.replace('{{DATASET_ID}}', dataset_id)
        
        try:
            client.query(sql_content).result()
            print(f"[OK] DEPLOYED: {view_name}")
        except Exception as e:
            print(f"[ERR] FAILED:   {view_name} | {e}")

    print("=" * 70)
    print("[FINISH] Infrastructure is now ready for Looker Studio.\n")

if __name__ == "__main__":
    deploy_views()

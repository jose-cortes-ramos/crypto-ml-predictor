import os
from google.cloud import bigquery
from dotenv import load_dotenv

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
load_dotenv(os.path.join(ROOT_DIR, '.env'))

def inspect_ml_results():
    project_id = os.getenv('GCP_PROJECT_ID')
    dataset_id = os.getenv('GCP_DATASET_ID')
    client = bigquery.Client(project=project_id)
    
    query = f"SELECT * FROM `{project_id}.{dataset_id}.crypto_ml_predictions` LIMIT 5"
    try:
        df = client.query(query).to_dataframe()
        print("\n--- MUESTRA REAL DE DATOS DE ML ---")
        print(df.to_string())
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_ml_results()

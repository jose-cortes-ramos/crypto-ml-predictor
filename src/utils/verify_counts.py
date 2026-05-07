import os
from google.cloud import bigquery
from dotenv import load_dotenv

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
load_dotenv(os.path.join(ROOT_DIR, '.env'))

def verify_data_counts():
    project_id = os.getenv('GCP_PROJECT_ID')
    dataset_id = os.getenv('GCP_DATASET_ID')
    client = bigquery.Client(project=project_id)
    
    tables = ["crypto_historical_trends", "crypto_historical_analytics", "crypto_ml_predictions"]
    
    print(f"VERIFICACIÓN DE CONTEO REAL - PROYECTO: {project_id}")
    print("=" * 60)

    for t in tables:
        query = f"SELECT COUNT(*) as total FROM `{project_id}.{dataset_id}.{t}`"
        try:
            results = client.query(query).to_dataframe()
            count = results['total'].iloc[0]
            print(f"TABLA: {t:30} | REGISTROS REALES: {count}")
        except Exception as e:
            print(f"[ERROR] No se pudo consultar la tabla {t}: {e}")

if __name__ == "__main__":
    verify_data_counts()

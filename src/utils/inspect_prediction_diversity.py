import os
from google.cloud import bigquery
from dotenv import load_dotenv

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
load_dotenv(os.path.join(ROOT_DIR, '.env'))

def inspect_diversity():
    project_id = os.getenv('GCP_PROJECT_ID')
    dataset_id = os.getenv('GCP_DATASET_ID')
    client = bigquery.Client(project=project_id)
    
    query = f"""
    SELECT 
        id,
        ml_prediction, 
        COUNT(*) as count,
        AVG(ml_probability) as avg_prob,
        MIN(ml_probability) as min_prob,
        MAX(ml_probability) as max_prob
    FROM `{project_id}.{dataset_id}.crypto_ml_predictions`
    GROUP BY id, ml_prediction
    ORDER BY id, ml_prediction
    """
    
    try:
        df = client.query(query).to_dataframe()
        print("\n=== AUDITORÍA DE DIVERSIDAD DE PREDICCIONES ===")
        print(df.to_string(index=False))
        
        # Muestra rápida de casos donde ml_prediction = 1
        print("\n--- EJEMPLOS DE SEÑALES POSITIVAS (1) ---")
        query_pos = f"SELECT id, ds, ml_probability FROM `{project_id}.{dataset_id}.crypto_ml_predictions` WHERE ml_prediction = 1 LIMIT 5"
        print(client.query(query_pos).to_dataframe().to_string(index=False))
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_diversity()

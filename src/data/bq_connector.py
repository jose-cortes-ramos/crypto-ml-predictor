import os
import pandas as pd
from google.cloud import bigquery
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BigQueryConnector:
    """
    Handles secure connectivity and data ingestion from GCP BigQuery.
    Following the Medallion architecture, it pulls data from Gold datasets.
    """
    
    def __init__(self):
        self.project_id = os.getenv('GCP_PROJECT_ID')
        self.dataset_id = os.getenv('GCP_DATASET_ID')
        self.table_id = os.getenv('GCP_TABLE_ID')
        
        # Senior Tip: Robust path handling for Notebooks
        creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if creds_path and not os.path.exists(creds_path):
            # Try one level up if not found (common for notebooks)
            alt_path = os.path.join('..', creds_path)
            if os.path.exists(alt_path):
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = alt_path
                print(f"[INFO] Adjusted credentials path for notebook context: {alt_path}")

        self.client = bigquery.Client(project=self.project_id)

    def fetch_historical_trends(self) -> pd.DataFrame:
        """
        Retrieves historical crypto trends from the Gold dataset.
        """
        query = f"""
            SELECT *
            FROM `{self.project_id}.{self.dataset_id}.{self.table_id}`
            ORDER BY ds DESC
        """
        print(f"Executing query on: {self.project_id}.{self.dataset_id}.{self.table_id}")
        return self.client.query(query).to_dataframe()

if __name__ == "__main__":
    # Smoke test for BigQuery connectivity
    try:
        connector = BigQueryConnector()
        print("[+] Connector initialized successfully.")
        
        # Attempt to fetch a small sample
        print("[+] Testing data extraction (limit 5)...")
        sample_data = connector.fetch_historical_trends().head(5)
        
        if not sample_data.empty:
            print("[SUCCESS] Data extraction verified. Sample head:")
            print(sample_data)
        else:
            print("[WARNING] Connection successful but table appears to be empty.")
            
    except Exception as e:
        print(f"[ERROR] Connection test FAILED: {e}")
        print("\nSenior Tip: Check if your Service Account has 'BigQuery Data Viewer' permissions.")

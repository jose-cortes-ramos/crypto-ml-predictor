import os
from google.cloud import bigquery
from dotenv import load_dotenv

load_dotenv()

def inspect_table_schema():
    """
    Retrieves the actual schema of the BigQuery table to identify correct column names.
    """
    project_id = os.getenv('GCP_PROJECT_ID')
    dataset_id = os.getenv('GCP_DATASET_ID')
    table_id = os.getenv('GCP_TABLE_ID')
    
    client = bigquery.Client(project=project_id)
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    
    print(f"Inspecting schema for: {table_ref}...")
    try:
        table = client.get_table(table_ref)
        print("\n[SUCCESS] Table found. Columns available:")
        for field in table.schema:
            print(f" - {field.name} ({field.field_type})")
    except Exception as e:
        print(f"[ERROR] Could not retrieve schema: {e}")

if __name__ == "__main__":
    inspect_table_schema()

import os
from google.cloud import bigquery
from dotenv import load_dotenv

# Path configuration
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
load_dotenv(os.path.join(ROOT_DIR, '.env'))

def audit_full_project():
    """
    Performs a global audit of the GCP project, listing all datasets, 
    tables, and their respective schemas following corporate standards.
    """
    project_id = os.getenv('GCP_PROJECT_ID')
    print(f"REPORT: GLOBAL PROJECT AUDIT - PROJECT: {project_id}")
    print("=" * 60)
    
    if not project_id:
        print("ERROR: GCP_PROJECT_ID not found in environment configuration.")
        return

    client = bigquery.Client(project=project_id)
    
    try:
        # 1. List all Datasets
        datasets = list(client.list_datasets())
        if not datasets:
            print(f"No datasets found for project: {project_id}")
            return

        for dataset in datasets:
            dataset_id = dataset.dataset_id
            print(f"\nDATASET: {dataset_id}")
            print("-" * 60)

            # 2. List all tables in dataset
            tables = list(client.list_tables(dataset_id))
            if not tables:
                print("  Status: Empty Dataset (No tables found)")
                continue

            for table_item in tables:
                table_ref = f"{project_id}.{dataset_id}.{table_item.table_id}"
                print(f"\n  TABLE: {table_item.table_id}")
                
                # 3. Retrieve Table Schema
                table = client.get_table(table_ref)
                print(f"  {'Field Name':25} | {'Data Type':15}")
                print(f"  {'-'*25} | {'-'*15}")
                for field in table.schema:
                    print(f"  {field.name:25} | {field.field_type:15}")
                print(f"  Summary: {table.num_rows} records found.")

    except Exception as e:
        print(f"CRITICAL ERROR: Global audit execution failed: {e}")

if __name__ == "__main__":
    audit_full_project()

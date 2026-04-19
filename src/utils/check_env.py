import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_environment():
    """
    Verifies that all required variables for BigQuery and MLOps are correctly loaded.
    """
    required_vars = [
        'GCP_PROJECT_ID', 
        'GCP_DATASET_ID', 
        'GCP_TABLE_ID', 
        'GOOGLE_APPLICATION_CREDENTIALS', 
        'MLFLOW_TRACKING_URI'
    ]
    
    print("Starting Senior Engineer Environment Check...")
    missing = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing.append(var)
            print(f"[-] MISSING: {var}")
        else:
            # Masking value for security reasons
            masked = value[:4] + "*" * (len(value) - 4) if value else "Empty"
            print(f"[+] LOADED: {var} = {masked}")
            
    if not missing:
        print("\n[SUCCESS] Environment variables are correctly configured.")
        # Check if service account file exists
        creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if os.path.exists(creds_path):
            print(f"[SUCCESS] GCP Credentials file found at: {creds_path}")
        else:
            print(f"[WARNING] GCP Credentials file NOT FOUND at: {creds_path}")
    else:
        print(f"\n[ERROR] Environment check FAILED. Missing: {', '.join(missing)}")

if __name__ == "__main__":
    check_environment()

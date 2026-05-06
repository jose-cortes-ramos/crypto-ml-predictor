import mlflow
import pandas as pd

def get_most_stable_model(experiment_name="crypto-momentum-xgboost"):
    """
    Centralized logic to discover the best performing model.
    Ensures consistency across the entire pipeline.
    """
    print(f"[+] Discovering champion model in: {experiment_name}")
    
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if not experiment:
        raise Exception(f"Experiment {experiment_name} not found.")

    runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id])
    if runs.empty:
        raise Exception("No runs found in MLflow.")

    # Identify precision columns
    precision_cols = [c for c in runs.columns if 'metrics.precision_fold_' in c]
    if not precision_cols:
        # Fallback to the latest run if no cross-val metrics exist
        return f"runs:/{runs.iloc[0].run_id}/production_model"
    
    # Stability Score calculation
    runs['mean_precision'] = runs[precision_cols].mean(axis=1)
    runs['std_precision'] = runs[precision_cols].std(axis=1).fillna(0)
    runs['stability_score'] = runs['mean_precision'] - runs['std_precision']

    best_run = runs.sort_values('stability_score', ascending=False).iloc[0]
    
    print(f"[SUCCESS] Champion discovered: {best_run.run_id} (Stability: {best_run.stability_score:.4f})")
    
    artifact_name = "momentum_model_v3" if "momentum" in experiment.name else "production_model"
    return f"runs:/{best_run.run_id}/{artifact_name}"

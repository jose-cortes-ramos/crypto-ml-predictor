CREATE OR REPLACE VIEW `{{PROJECT_ID}}.{{DATASET_ID}}.v_dashboard_scatter` AS
SELECT
  CAST(ds AS DATE) as fecha,
  id as crypto_id,
  ROUND(ml_probability * 100, 1) as confianza_pct,
  ROUND(return_t30 * 100, 1) as retorno_30d_pct,
  ROUND(ml_volume_zscore, 2) as zscore_magnitud,
  CASE WHEN ml_prediction = 1 THEN 'GREEN' ELSE 'RED' END as prediccion
FROM `{{PROJECT_ID}}.{{DATASET_ID}}.vw_looker_master_intelligence`
WHERE ml_volume_zscore >= 2.0
  AND return_t30 IS NOT NULL;

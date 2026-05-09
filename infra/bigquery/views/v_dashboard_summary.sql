CREATE OR REPLACE VIEW `{{PROJECT_ID}}.{{DATASET_ID}}.v_dashboard_summary` AS
-- Esta vista alimenta el resumen informativo y la auditoría global
SELECT
  'Total Registros' as metric_label,
  CAST(COUNT(*) AS STRING) as metric_value
FROM `{{PROJECT_ID}}.{{DATASET_ID}}.vw_looker_master_intelligence`

UNION ALL

SELECT
  'Tsunamis Detectados',
  CAST(COUNTIF(ml_volume_zscore >= 2.0) AS STRING)
FROM `{{PROJECT_ID}}.{{DATASET_ID}}.vw_looker_master_intelligence`

UNION ALL

SELECT
  'Tsunamis GREEN',
  CAST(COUNTIF(ml_prediction = 1 AND ml_volume_zscore >= 2.0) AS STRING)
FROM `{{PROJECT_ID}}.{{DATASET_ID}}.vw_looker_master_intelligence`

UNION ALL

SELECT
  'Tsunamis RED',
  CAST(COUNTIF(ml_prediction = 0 AND ml_volume_zscore >= 2.0) AS STRING)
FROM `{{PROJECT_ID}}.{{DATASET_ID}}.vw_looker_master_intelligence`

UNION ALL

SELECT
  'Última Actualización',
  CAST(MAX(ds) AS STRING)
FROM `{{PROJECT_ID}}.{{DATASET_ID}}.vw_looker_master_intelligence`;

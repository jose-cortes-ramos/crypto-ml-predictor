CREATE OR REPLACE VIEW `{{PROJECT_ID}}.{{DATASET_ID}}.v_dashboard_kpis` AS
-- Esta vista alimenta las 3 tarjetas grandes de la fila superior
SELECT
  'Precisión GREEN' as metric_name,
  ROUND(
    COUNTIF(
      ml_prediction = 1 
      AND return_t30 > 0.05
    ) * 100.0 / NULLIF(COUNTIF(ml_prediction = 1), 0),
    1
  ) as metric_value
FROM `{{PROJECT_ID}}.{{DATASET_ID}}.vw_looker_master_intelligence`
WHERE return_t30 IS NOT NULL

UNION ALL

SELECT
  'Precisión RED' as metric_name,
  ROUND(
    COUNTIF(
      ml_prediction = 0 
      AND return_t30 < -0.05
    ) * 100.0 / NULLIF(COUNTIF(ml_prediction = 0), 0),
    1
  ) as metric_value
FROM `{{PROJECT_ID}}.{{DATASET_ID}}.vw_looker_master_intelligence`
WHERE return_t30 IS NOT NULL

UNION ALL

SELECT
  'Cobertura (%)',
  ROUND(
    COUNTIF(ml_volume_zscore >= 2.0) * 100.0 / COUNT(*),
    1
  ) as metric_value
FROM `{{PROJECT_ID}}.{{DATASET_ID}}.vw_looker_master_intelligence`;

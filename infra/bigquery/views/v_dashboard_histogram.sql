CREATE OR REPLACE VIEW `{{PROJECT_ID}}.{{DATASET_ID}}.v_dashboard_histogram` AS
WITH trend_buckets AS (
  SELECT
    ROUND(ml_trend_ratio * 10) / 10 as trend_bucket,
    COUNT(*) as evento_count,
    CASE
      WHEN ml_trend_ratio < 0.85 THEN 'GREEN'
      WHEN ml_trend_ratio >= 1.05 THEN 'RED'
      ELSE 'NEUTRAL'
    END as bucket_color,
    ROUND(AVG(return_t30) * 100, 2) as avg_retorno
  FROM `{{PROJECT_ID}}.{{DATASET_ID}}.vw_looker_master_intelligence`
  WHERE ml_volume_zscore >= 2.0
    AND return_t30 IS NOT NULL
  GROUP BY 1, 3
)
SELECT
  trend_bucket,
  evento_count,
  bucket_color,
  avg_retorno
FROM trend_buckets
ORDER BY trend_bucket ASC;

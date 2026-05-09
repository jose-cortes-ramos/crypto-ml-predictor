CREATE OR REPLACE VIEW `{{PROJECT_ID}}.{{DATASET_ID}}.v_dashboard_table_tsunamis` AS
SELECT
  CAST(ds AS DATE) as fecha,
  id as crypto_id,
  CASE WHEN ml_prediction = 1 THEN 'GREEN' ELSE 'RED' END as prediccion,
  ROUND(ml_probability * 100, 1) as confianza_pct,
  ROUND(ml_volume_zscore, 2) as zscore,
  ROUND(ml_trend_ratio, 3) as trend_ratio,
  ROUND(total_volume, 0) as volumen_usd,
  ROUND(price, 2) as precio_usd,
  ROUND(return_t30 * 100, 2) as retorno_30d_pct,
  CASE
    WHEN ml_prediction = 1 AND ml_probability > 0.60 THEN 'COMPRA FUERTE'
    WHEN ml_prediction = 1 THEN 'COMPRA'
    WHEN ml_prediction = 0 AND ml_probability > 0.60 THEN 'VENTA/COBERTURA'
    ELSE 'VENTA'
  END as accion_recomendada,
  CASE
    WHEN ml_prediction = 1 AND return_t30 > 0.05 THEN 'SUCCESS'
    WHEN ml_prediction = 0 AND return_t30 < -0.05 THEN 'SUCCESS'
    ELSE 'FAILURE'
  END as resultado_real
FROM `{{PROJECT_ID}}.{{DATASET_ID}}.vw_looker_master_intelligence`
WHERE ml_volume_zscore >= 2.0
  AND return_t30 IS NOT NULL
ORDER BY ml_volume_zscore DESC
LIMIT 20;

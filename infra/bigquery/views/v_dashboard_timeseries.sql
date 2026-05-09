CREATE OR REPLACE VIEW `{{PROJECT_ID}}.{{DATASET_ID}}.v_dashboard_timeseries` AS
SELECT
  CAST(ds AS DATE) as fecha,
  ds as timestamp_evento,
  id as crypto_id,
  
  -- Panel 1: Precio
  ROUND(price, 2) as price,
  
  -- Panel 2: Volumen con color
  ROUND(total_volume, 0) as total_volume,
  CASE
    WHEN ml_volume_zscore >= 2.0 THEN 'Tsunami'
    ELSE 'Normal'
  END as volumen_tipo,
  
  -- Panel 3: Z-Score con colores
  ROUND(ml_volume_zscore, 2) as ml_volume_zscore,
  ROUND(ml_trend_ratio, 3) as ml_trend_ratio,
  
  -- Color condicional para barras
  CASE
    WHEN ml_volume_zscore >= 2.0 AND ml_trend_ratio < 0.85 THEN 'GREEN'
    WHEN ml_volume_zscore >= 2.0 AND ml_trend_ratio >= 1.05 THEN 'RED'
    WHEN ml_volume_zscore >= 2.0 THEN 'NEUTRAL'
    ELSE 'Normal'
  END as zscore_color,
  
  -- Métrica de predicción
  ml_prediction,
  ROUND(ml_probability * 100, 1) as ml_probability_pct,
  
  -- Validación
  ROUND(return_t30 * 100, 2) as return_t30_pct

FROM `{{PROJECT_ID}}.{{DATASET_ID}}.vw_looker_master_intelligence`
ORDER BY ds DESC;

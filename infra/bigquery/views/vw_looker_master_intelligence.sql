CREATE OR REPLACE VIEW `{{PROJECT_ID}}.{{DATASET_ID}}.vw_looker_master_intelligence` AS
SELECT 
    t.id,
    t.ds,
    t.price,
    t.total_volume,
    t.market_cap_dominance,
    -- Analytics Layer
    a.avg_price_next_7d,
    a.global_avg_volume,
    a.global_avg_price,
    -- ML Intelligence Layer
    p.zscore_30d as ml_volume_zscore,
    p.price_vs_ma30 as ml_trend_ratio,
    p.ml_prediction,
    p.ml_probability,
    -- Forensic Metrics
    (LEAD(t.price, 30) OVER(PARTITION BY t.id ORDER BY t.ds ASC) - t.price) / t.price as return_t30
FROM 
    `{{PROJECT_ID}}.{{DATASET_ID}}.crypto_historical_trends` as t
LEFT JOIN 
    `{{PROJECT_ID}}.{{DATASET_ID}}.crypto_historical_analytics` as a
    ON t.id = a.id AND t.ds = a.ds
LEFT JOIN 
    `{{PROJECT_ID}}.{{DATASET_ID}}.crypto_ml_predictions` as p
    ON t.id = p.id AND t.ds = p.ds;

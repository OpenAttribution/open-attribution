CREATE MATERIALIZED VIEW user_dx_attributed_mv TO user_dx_attributed
AS 
SELECT 
    uda.install_date,
    ai.store_id,
    ai.network,
    ai.campaign_name,
    ai.campaign_id,
    ai.ad_name,
    ai.ad_id,
    ai.country_iso,
    ai.state_iso,
    ai.city_name,
    sum(CASE WHEN uda.dx = 1 THEN 1 ELSE 0 END) as dx_1,
    sum(CASE WHEN uda.dx = 2 THEN 1 ELSE 0 END) as dx_2,
    sum(CASE WHEN uda.dx = 3 THEN 1 ELSE 0 END) as dx_3,
    sum(CASE WHEN uda.dx = 4 THEN 1 ELSE 0 END) as dx_4,
    sum(CASE WHEN uda.dx = 5 THEN 1 ELSE 0 END) as dx_5,
    sum(CASE WHEN uda.dx = 6 THEN 1 ELSE 0 END) as dx_6,
    sum(CASE WHEN uda.dx = 7 THEN 1 ELSE 0 END) as dx_7,
    sum(CASE WHEN uda.dx = 15 THEN 1 ELSE 0 END) as dx_15,
    sum(CASE WHEN uda.dx = 30 THEN 1 ELSE 0 END) as dx_30,
    sum(CASE WHEN uda.dx = 60 THEN 1 ELSE 0 END) as dx_60,
    sum(CASE WHEN uda.dx = 90 THEN 1 ELSE 0 END) as dx_90,
    sum(CASE WHEN uda.dx = 180 THEN 1 ELSE 0 END) as dx_180,
    sum(CASE WHEN uda.dx = 365 THEN 1 ELSE 0 END) as dx_365
FROM user_dx_activity uda
LEFT JOIN attributed_installs ai ON uda.oa_uid = ai.oa_uid
GROUP BY 
    uda.install_date,
    ai.store_id,
    ai.network,
    ai.campaign_name,
    ai.campaign_id,
    ai.ad_name,
    ai.ad_id,
    ai.country_iso,
    ai.state_iso,
    ai.city_name
ORDER BY install_date, store_id, network, campaign_name, campaign_id, ad_name, ad_id, country_iso, state_iso, city_name;
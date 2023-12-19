CREATE MATERIALIZED VIEW daily_overview_attributed_installs_mv
TO daily_overview
AS
SELECT
    toDate(app_event_time) AS on_date,
    store_id,
    network,
    campaign_name,
    campaign_id,
    ad_name,
    ad_id,
    count() AS installs,
    sum(revenue) as revenue
FROM
    attributed_installs
GROUP BY
    toDate(app_event_time) AS on_date,
    store_id,
    network,
    campaign_name,
    campaign_id,
    ad_name,
    ad_id
;




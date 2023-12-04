CREATE MATERIALIZED VIEW daily_overview_impressions_mv
TO daily_overview
AS
SELECT
    toDate(event_time) AS on_date,
    store_id,
    network,
    campaign_name,
    campaign_id,
    ad_name,
    ad_id,
    count() AS impressions
FROM
    impressions
GROUP BY
    toDate(event_time) AS on_date,
    store_id,
    network,
    campaign_name,
    campaign_id,
    ad_name,
    ad_id
;




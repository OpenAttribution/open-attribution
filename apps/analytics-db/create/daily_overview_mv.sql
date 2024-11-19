CREATE MATERIALIZED VIEW daily_overview_mv
REFRESH EVERY 5 SECOND
TO daily_overview
AS
WITH combined AS (
    (
        SELECT
            toDate(event_time) AS on_date,
            store_id,
            network,
            campaign_name,
            campaign_id,
            ad_name,
            ad_id,
            count() AS impressions,
            0 AS clicks,
            0 AS installs,
            0 AS revenue
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
    )
UNION ALL
(
    SELECT
            toDate(event_time) AS on_date,
            store_id,
            network,
            campaign_name,
            campaign_id,
            ad_name,
            ad_id,
            0 AS impressions,
            count() AS clicks,
            0 AS installs,
            0 AS revenue
    FROM
            clicks
    GROUP BY
            toDate(event_time) AS on_date,
            store_id,
            network,
            campaign_name,
            campaign_id,
            ad_name,
            ad_id
)
UNION ALL
(
SELECT
            toDate(app_event_time) AS on_date,
            store_id,
            network,
            campaign_name,
            campaign_id,
            ad_name,
            ad_id,
            0 AS impressions,
            0 AS clicks,
            count() AS installs,
            0 AS revenue
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
)
UNION ALL
(
SELECT 
    toDate(install_time) as on_date,
    store_id,
    'Organic' as network,
    '' as campaign_name,
    '' as campaign_id,
    '' as ad_name,
    '' as ad_id,
    0 AS impressions,
    0 AS clicks,
    count() AS installs,
    0 AS revenue
FROM installs_base ib WHERE ib.event_uid not in (SELECT event_uid FROM attributed_installs)
GROUP BY
    toDate(install_time) AS on_date,
    store_id,
    network,
    campaign_name,
    campaign_id,
    ad_name,
    ad_id
)
)
SELECT
    on_date,
    store_id,
    network,
    campaign_name,
    campaign_id,
    ad_name,
    ad_id,
    sum(impressions) AS impressions,
    sum(clicks) AS clicks,
    sum(installs) AS installs,
    sum(revenue) AS revenue
FROM
    combined
GROUP BY
    on_date,
    store_id,
    network,
    campaign_name,
    campaign_id,
    ad_name,
    ad_id;

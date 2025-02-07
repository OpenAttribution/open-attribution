CREATE MATERIALIZED VIEW daily_overview_mv
REFRESH EVERY 1 MINUTE
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
            country_iso,
            count() AS impressions,
            0 AS clicks,
            0 AS installs,
            0 AS revenue,
            0 AS dx_1,
            0 AS dx_2,
            0 AS dx_3,
            0 AS dx_4,
            0 AS dx_5,
            0 AS dx_6,
            0 AS dx_7,
            0 AS dx_15,
            0 AS dx_30,
            0 AS dx_60,
            0 AS dx_90,
            0 AS dx_180,
            0 AS dx_365
        FROM
            impressions
        GROUP BY
            toDate(event_time) AS on_date,
            store_id,
            network,
            campaign_name,
            campaign_id,
            ad_name,
            ad_id,
            country_iso
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
            country_iso,
            0 AS impressions,
            count() AS clicks,
            0 AS installs,
            0 AS revenue,
            0 AS dx_1,
            0 AS dx_2,
            0 AS dx_3,
            0 AS dx_4,
            0 AS dx_5,
            0 AS dx_6,
            0 AS dx_7,
            0 AS dx_15,
            0 AS dx_30,
            0 AS dx_60,
            0 AS dx_90,
            0 AS dx_180,
            0 AS dx_365
    FROM
            clicks
    GROUP BY
            toDate(event_time) AS on_date,
            store_id,
            network,
            campaign_name,
            campaign_id,
            ad_name,
            ad_id,
            country_iso
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
            country_iso,
            0 AS impressions,
            0 AS clicks,
            count() AS installs,
            0 AS revenue,
            0 AS dx_1,
            0 AS dx_2,
            0 AS dx_3,
            0 AS dx_4,
            0 AS dx_5,
            0 AS dx_6,
            0 AS dx_7,
            0 AS dx_15,
            0 AS dx_30,
            0 AS dx_60,
            0 AS dx_90,
            0 AS dx_180,
            0 AS dx_365
FROM
            attributed_installs
GROUP BY
            toDate(app_event_time) AS on_date,
            store_id,
            network,
            campaign_name,
            campaign_id,
            ad_name,
            ad_id,
            country_iso
)
UNION ALL
(
SELECT
    install_date AS on_date,
    store_id,
    network,
    campaign_name,
    campaign_id,
    ad_name,
    ad_id,
    country_iso,
    0 AS impressions,
    0 AS clicks,
    0 AS installs,
    0 AS revenue,
    sum(dx_1) AS dx_1,
    sum(dx_2) AS dx_2,
    sum(dx_3) AS dx_3,
    sum(dx_4) AS dx_4,
    sum(dx_5) AS dx_5,
    sum(dx_6) AS dx_6,
    sum(dx_7) AS dx_7,
    sum(dx_15) AS dx_15,
    sum(dx_30) AS dx_30,
    sum(dx_60) AS dx_60,
    sum(dx_90) AS dx_90,
    sum(dx_180) AS dx_180,
    sum(dx_365) AS dx_365
FROM
    user_dx_attributed
GROUP BY
    install_date AS on_date,
    store_id,
    network,
    campaign_name,
    campaign_id,
    ad_name,
    ad_id,
    country_iso
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
    country_iso,
    sum(impressions) AS impressions,
    sum(clicks) AS clicks,
    sum(installs) AS installs,
    sum(revenue) AS revenue,
    sum(dx_1) AS dx_1,
    sum(dx_2) AS dx_2,
    sum(dx_3) AS dx_3,
    sum(dx_4) AS dx_4,
    sum(dx_5) AS dx_5,
    sum(dx_6) AS dx_6,
    sum(dx_7) AS dx_7,
    sum(dx_15) AS dx_15,
    sum(dx_30) AS dx_30,
    sum(dx_60) AS dx_60,
    sum(dx_90) AS dx_90,
    sum(dx_180) AS dx_180,
    sum(dx_365) AS dx_365
FROM
    combined
GROUP BY
    on_date,
    store_id,
    network,
    campaign_name,
    campaign_id,
    ad_name,
    ad_id,
    country_iso
    ;

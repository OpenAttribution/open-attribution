CREATE MATERIALIZED VIEW daily_overview_mv
TO daily_overview
AS
SELECT
    toDate(app_event_time) AS on_date,
    ae.store_id,
    ae.network,
    ae.campaign_name,
    ae.campaign_id,
    ae.ad_name,
    ae.ad_id,
    COALESCE(
        i.impressions,
        0
    ) AS impressions,
    COALESCE(
        c.clicks,
        0
    ) AS clicks,
    count() AS installs,
    sum(ae.revenue) AS revenue
FROM
    attributed_events ae
LEFT JOIN (
        SELECT
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
            store_id,
            network,
            campaign_name,
            campaign_id,
            ad_name,
            ad_id
    ) i ON
    ae.store_id = i.store_id
    AND ae.network = i.network
    AND ae.campaign_name = i.campaign_name
    AND ae.campaign_id = i.campaign_id
    AND ae.ad_name = i.ad_name
    AND ae.ad_id = i.ad_id
LEFT JOIN (
        SELECT
            store_id,
            network,
            campaign_name,
            campaign_id,
            ad_name,
            ad_id,
            count() AS clicks
        FROM
            clicks
        GROUP BY
            store_id,
            network,
            campaign_name,
            campaign_id,
            ad_name,
            ad_id
    ) c ON
    ae.store_id = c.store_id
    AND ae.network = c.network
    AND ae.campaign_name = c.campaign_name
    AND ae.campaign_id = c.campaign_id
    AND ae.ad_name = c.ad_name
    AND ae.ad_id = c.ad_id
GROUP BY
    on_date,
    ae.store_id,
    ae.network,
    ae.campaign_name,
    ae.campaign_id,
    ae.ad_name,
    ae.ad_id,
    i.impressions,
    c.clicks
    ;


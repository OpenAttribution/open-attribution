CREATE MATERIALIZED VIEW attribute_clicks_mv
REFRESH EVERY 5 SECOND
TO attributed_clicks AS
WITH
merged_click_event AS (
    -- Ranked rows by click time
    SELECT 
            app.event_time AS app_event_time,
            app.store_id AS store_id,
            app.event_id,
            app.ifa,
            app.client_ip,
            app.event_uid,
            'click' AS attribution_type,
            click.event_time AS attribution_event_time,
            click.network,
            click.campaign_name,
            click.campaign_id,
            click.ad_name,
            click.ad_id,
            click.link_uid,
            app.revenue,
            ROW_NUMBER() OVER (
                PARTITION BY app.client_ip,
            app.ifa
        ORDER BY
            -- Sorted by earliest app events but latest click
            app_event_time ASC,
            click.event_time DESC
        ) AS event_and_click_rn
    FROM 
            (
            SELECT 
                    *,
                    MIN(event_time) OVER (
                        PARTITION BY client_ip,
                        ifa
                ) AS earliest_app_event_time
            FROM 
                    events
            WHERE 
                    event_id = 'app_open'
        ) app
    LEFT JOIN 
            (
            SELECT 
                    *
            FROM 
                    default.clicks
        ) click
        ON 
            app.client_ip = click.client_ip
        AND app.ifa = click.ifa
    WHERE 
            click.event_time < app.earliest_app_event_time
        -- TODO: This will need to be parameterized
        AND click.event_time >= app.earliest_app_event_time - INTERVAL 7 DAY
),
latest_attributed_click_events AS (
    SELECT
        *
    FROM
        merged_click_event
    WHERE
        event_and_click_rn = 1
)
SELECT
    -- All rows except rn
    app_event_time,
    store_id,
    event_id,
    ifa,
    client_ip,
    attribution_type,
    attribution_event_time,
    link_uid,
    event_uid,
    network,
    campaign_name,
    campaign_id,
    ad_name,
    ad_id,
    0 as revenue
FROM
    latest_attributed_click_events
;

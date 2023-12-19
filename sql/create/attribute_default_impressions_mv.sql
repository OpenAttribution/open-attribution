CREATE MATERIALIZED VIEW attribute_default_impressions_mv
TO attributed_installs -- Specify the destination table
AS
WITH
merged_impression_event AS (
    -- Ranked rows by impression time
    SELECT 
            app.event_time AS app_event_time,
            app.store_id AS store_id,
            app.event_id,
            app.ifa,
            app.client_ip,
            app.event_uid,
            'impression' AS attribution_type,
            impression.event_time AS attribution_event_time,
            impression.network,
            impression.campaign_name,
            impression.campaign_id,
            impression.ad_name,
            impression.ad_id,
            impression.link_uid,
            app.revenue,
            ROW_NUMBER() OVER (
                PARTITION BY app.client_ip,
            app.ifa
        ORDER BY
            impression.event_time DESC
        ) AS rn
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
                    default.impressions
        ) impression
        ON 
            app.client_ip = impression.client_ip
        AND app.ifa = impression.ifa
    WHERE 
            impression.event_time <= app.earliest_app_event_time
        -- TODO: This will need to be parameterized
        AND impression.event_time >= app.earliest_app_event_time - INTERVAL 1 DAY
),
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
            click.event_time DESC
        ) AS rn
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
            click.event_time <= app.earliest_app_event_time
        -- TODO: This will need to be parameterized
        AND click.event_time >= now() - INTERVAL 7 DAY
),
latest_attributed_click_events AS (
    SELECT
        *
    FROM
        merged_click_event
    WHERE
        rn = 1
),
latest_attributed_impression_events AS (
    SELECT
        *
    FROM
        merged_impression_event mie
    WHERE
        rn = 1
        AND mie.ifa NOT IN (
            SELECT
                DISTINCT ifa
            FROM
                latest_attributed_click_events
        )
)
SELECT
    -- All rows except rn
    app_event_time,
    store_id,
    event_id,
    ifa,
    client_ip,
    event_uid,
    attribution_type,
    attribution_event_time,
    network,
    campaign_name,
    campaign_id,
    ad_name,
    ad_id,
    link_uid
FROM
    latest_attributed_impression_events
;

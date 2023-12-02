CREATE MATERIALIZED VIEW attributed_events_mv
TO attributed_events -- Specify the destination table
AS
SELECT 
    app.event_time AS app_event_time,
    app.store_id AS store_id,
    app.event_id,
    app.ifa,
    app.client_ip,
    click.event_time AS click_event_time,
    click.network,
    click.campaign_name,
    click.campaign_id,
    click.ad_name,
    click.ad_id,
    app.revenue
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
            *,
            argMax(
                event_time,
                event_time
            ) OVER (
                PARTITION BY client_ip,
                ifa
            ORDER BY
                event_time DESC
            ) AS latest_click_time
        FROM 
            clicks
    ) click
ON 
    app.client_ip = click.client_ip
    AND app.ifa = click.ifa
WHERE 
    click.event_time <= app.earliest_app_event_time
    AND click.latest_click_time = click.event_time
    ;


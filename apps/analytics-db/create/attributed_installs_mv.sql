CREATE MATERIALIZED VIEW attribute_installs_mv
REFRESH EVERY 1 MINUTE
TO attributed_installs
AS
SELECT 
    app_event_time,
    store_id,
    event_id,
    ifa,
    client_ip,
    attribution_type,
    attribution_event_time,
    link_uid,
    oa_uid,
    event_uid,
    network,
    campaign_name,
    campaign_id,
    ad_name,
    ad_id,
    country_iso,
    state_iso,
    city_name
FROM attributed_clicks
UNION ALL
SELECT 
 app_event_time,
    store_id,
    event_id,
    ifa,
    client_ip,
    attribution_type,
    attribution_event_time,
    link_uid,
    oa_uid,
    event_uid,
    network,
    campaign_name,
    campaign_id,
    ad_name,
    ad_id,
    country_iso,
    state_iso,
    city_name
    FROM attributed_impressions
UNION ALL
SELECT 
    install_time as app_event_time,
    store_id,
    event_id,
    ifa,
    client_ip,
    'Organic' as attribution_type,
    install_time as attribution_event_time,
    null as link_uid,
    oa_uid,
    event_uid,
    'Organic' as network,
    'Organic' as campaign_name,
    'Organic' as campaign_id,
    'Organic' as ad_name,
    'Organic' as ad_id,
    country_iso,
    state_iso,
    city_name
 FROM installs_base
WHERE oa_uid not in (SELECT oa_uid FROM attributed_clicks)
OR oa_uid not in (SELECT oa_uid FROM attributed_impressions)
;

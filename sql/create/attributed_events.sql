CREATE TABLE attributed_events
(
    app_event_time DateTime64(3, 'UTC'),
    store_id LowCardinality(String),
    event_id LowCardinality(String),
    ifa UUID,
    client_ip String,
    click_event_time DateTime64(3, 'UTC'),
    network LowCardinality(String),
    campaign_name LowCardinality(String),
    campaign_id LowCardinality(String),
    ad_name LowCardinality(String),
    ad_id LowCardinality(String),
    revenue Nullable(Decimal32(4))
) ENGINE = MergeTree ORDER BY (store_id, event_id, ifa, client_ip, app_event_time)


CREATE TABLE attributed_events
(
    app_event_time DateTime64(3, 'UTC'),
    store_id LowCardinality(String),
    event_id LowCardinality(String),
    ifa UUID,
    client_ip String DEFAULT '',
    click_event_time DateTime64(3, 'UTC'),
    network LowCardinality(String) DEFAULT '',
    campaign_name LowCardinality(String) DEFAULT '',
    campaign_id LowCardinality(String) DEFAULT '',
    ad_name LowCardinality(String) DEFAULT '',
    ad_id LowCardinality(String) DEFAULT '',
    revenue Nullable(Decimal32(4)) DEFAULT 0
) ENGINE = MergeTree ORDER BY (store_id, event_id, ifa, client_ip, app_event_time)


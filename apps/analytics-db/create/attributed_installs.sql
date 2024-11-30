CREATE TABLE attributed_installs
(
    app_event_time DateTime64(3, Utc),
    store_id LowCardinality(String),
    event_id LowCardinality(String),
    ifa UUID,
    client_ip String DEFAULT '',
    attribution_type LowCardinality(String),
    attribution_event_time DateTime64(3, Utc),
    link_uid UUID,
    oa_uid UUID,
    event_uid UUID,
    network LowCardinality(String) DEFAULT '',
    campaign_name LowCardinality(String) DEFAULT '',
    campaign_id LowCardinality(String) DEFAULT '',
    ad_name LowCardinality(String) DEFAULT '',
    ad_id LowCardinality(String) DEFAULT '',
    country_iso LowCardinality(String) DEFAULT '',
    state_iso LowCardinality(String) DEFAULT '',
    city_name LowCardinality(String) DEFAULT '',
    revenue Nullable (Decimal (9, 4)) DEFAULT 0
)
ENGINE = MergeTree()
PRIMARY KEY (store_id, ifa, oa_uid)
ORDER BY (store_id, ifa, oa_uid, app_event_time);

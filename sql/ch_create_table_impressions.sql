CREATE TABLE impressions
(
    __time DateTime,
    store_id LowCardinality(String),
    network LowCardinality(String),
    campaign_name LowCardinality(String),
    campaign_id LowCardinality(String),
    ad_name LowCardinality(String),
    ad_id LowCardinality(String),
    ifa UUID,
    client_ip String,
) ENGINE = MergeTree ORDER BY (store_id, network, __time)


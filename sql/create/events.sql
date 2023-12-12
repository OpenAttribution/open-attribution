CREATE TABLE events
(
    event_time DateTime64(3, 'UTC'),
    store_id LowCardinality(String),
    event_id LowCardinality(String),
    revenue Nullable(Decimal32(4)),
    ifa UUID,
    client_ip String,
    event_uid UUID,
) ENGINE = MergeTree ORDER BY (store_id, event_id, event_time)


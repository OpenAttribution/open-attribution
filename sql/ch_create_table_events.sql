CREATE TABLE events
(
    __time DateTime,
    event_time DateTime,
    store_id LowCardinality(String),
    event_id LowCardinality(String),
    revenue Nullable(Decimal32(4)),
    ifa UUID,
    client_ip String,
) ENGINE = MergeTree ORDER BY (store_id, event_id, event_time)


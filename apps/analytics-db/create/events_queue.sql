CREATE TABLE events_queue
(
    event_time DateTime64(3, 'UTC'),
    store_id LowCardinality(String),
    event_id LowCardinality(String),
    revenue Nullable(Decimal32(4)),
    ifa UUID,
    oa_uid UUID,
    client_ip String,
    event_uid UUID,
    received_at DateTime64(3, 'UTC'),
)
ENGINE = Kafka('localhost:9092', 'events', 'clickhouse') 
            SETTINGS kafka_format = 'JSONEachRow', 
            kafka_thread_per_consumer = 0, 
            kafka_num_consumers = 1, 
            kafka_handle_error_mode = 'stream';


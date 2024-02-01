CREATE TABLE events_queue
(
    event_time DateTime64(3, 'UTC'),
    store_id LowCardinality(String),
    event_id LowCardinality(String),
    revenue Nullable(Decimal32(4)),
    ifa UUID,
    client_ip String,
    event_uid UUID,
) 
ENGINE = Kafka('localhost:9092', 'events', 'clickhouse',
            'JSONEachRow') settings kafka_thread_per_consumer = 0, kafka_num_consumers = 1;


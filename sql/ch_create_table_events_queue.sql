CREATE TABLE events_queue
(
    __time DateTime,
    event_time DateTime,
    store_id LowCardinality(String),
    event_id LowCardinality(String),
    revenue Nullable(Decimal32(4)),
    ifa UUID,
    client_ip String
) 
ENGINE = Kafka('localhost:9092', 'events', 'clickhouse',
            'JSONEachRow') settings kafka_thread_per_consumer = 0, kafka_num_consumers = 1;


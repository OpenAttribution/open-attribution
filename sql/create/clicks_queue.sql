CREATE TABLE clicks_queue
(
    event_time DateTime64(3, 'UTC'),
    store_id LowCardinality(String),
    network LowCardinality(String),
    campaign_name LowCardinality(String),
    campaign_id LowCardinality(String),
    ad_name LowCardinality(String),
    ad_id LowCardinality(String),
    ifa UUID,
    client_ip String,
    link_uid UUID,
) 
ENGINE = Kafka('localhost:9092', 'clicks', 'clickhouse',
            'JSONEachRow') settings kafka_thread_per_consumer = 0, kafka_num_consumers = 1;


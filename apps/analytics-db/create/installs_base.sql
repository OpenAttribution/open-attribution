CREATE TABLE installs_base
(
    install_time DateTime64(3, 'UTC'),
    store_id LowCardinality(String),
    event_id LowCardinality(String),
    ifa UUID,
    client_ip String,
    event_uid UUID,
    received_at DateTime64(3, 'UTC'),
)
ENGINE = MergeTree()
PRIMARY KEY (store_id, ifa, event_id)
ORDER BY (store_id, ifa, event_id, install_time);



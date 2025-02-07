CREATE TABLE installs_base
(
    install_time DateTime64(3, 'UTC'),
    store_id LowCardinality(String),
    event_id LowCardinality(String),
    ifa UUID,
    oa_uid UUID,
    client_ip String,
    country_iso LowCardinality(String),
    state_iso LowCardinality(String),
    city_name LowCardinality(String),
    event_uid UUID,
    received_at DateTime64(3, 'UTC'),
)
ENGINE = MergeTree()
PRIMARY KEY (store_id, ifa, oa_uid)
ORDER BY (store_id, ifa, oa_uid, install_time);



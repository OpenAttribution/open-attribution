CREATE TABLE attributed_installs
(
    app_event_time DATETIME64 (3, Utc),
    store_id LOWCARDINALITY (String),
    event_id LOWCARDINALITY (String),
    ifa UUID,
    client_ip STRING DEFAULT '',
    attribution_type LOWCARDINALITY (String),
    attribution_event_time DATETIME64 (3, Utc),
    link_uid UUID,
    event_uid UUID,
    network LOWCARDINALITY (String) DEFAULT '',
    campaign_name LOWCARDINALITY (String) DEFAULT '',
    campaign_id LOWCARDINALITY (String) DEFAULT '',
    ad_name LOWCARDINALITY (String) DEFAULT '',
    ad_id LOWCARDINALITY (String) DEFAULT '',
    revenue NULLABLE (DECIMAL(9, 4)) DEFAULT 0
)
ENGINE = MERGETREE()
PRIMARY KEY (store_id, ifa, client_ip)
ORDER BY (store_id, ifa, client_ip, event_id, app_event_time);

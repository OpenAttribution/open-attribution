CREATE TABLE daily_overview
(
    on_date Date,
    store_id LowCardinality(String),
    network LowCardinality(String),
    campaign_name LowCardinality(String),
    campaign_id LowCardinality(String),
    ad_name LowCardinality(String),
    ad_id LowCardinality(String),
    impressions SimpleAggregateFunction(Sum, UInt64),
    clicks SimpleAggregateFunction(Sum, UInt64),
    installs SimpleAggregateFunction(Sum, UInt64),
    revenue Nullable (SimpleAggregateFunction (Sum, Decimal (38, 4))) DEFAULT 0
) ENGINE = AggregatingMergeTree()
ORDER BY (
    on_date, store_id, network, campaign_name, campaign_id, ad_name, ad_id
);

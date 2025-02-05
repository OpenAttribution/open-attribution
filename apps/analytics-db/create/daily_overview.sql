CREATE TABLE daily_overview
(
    on_date Date,
    store_id LowCardinality(String),
    network LowCardinality(String),
    campaign_name LowCardinality(String),
    campaign_id LowCardinality(String),
    ad_name LowCardinality(String),
    ad_id LowCardinality(String),
    country_iso LowCardinality(String),
    impressions SimpleAggregateFunction(Sum, UInt64),
    clicks SimpleAggregateFunction(Sum, UInt64),
    installs SimpleAggregateFunction(Sum, UInt64),
    revenue Nullable (SimpleAggregateFunction (Sum, Decimal (38, 4))) DEFAULT 0,
    dx_1 SimpleAggregateFunction(Sum, UInt64),
    dx_2 SimpleAggregateFunction(Sum, UInt64),
    dx_3 SimpleAggregateFunction(Sum, UInt64),
    dx_4 SimpleAggregateFunction(Sum, UInt64),
    dx_5 SimpleAggregateFunction(Sum, UInt64),
    dx_6 SimpleAggregateFunction(Sum, UInt64),
    dx_7 SimpleAggregateFunction(Sum, UInt64),
    dx_15 SimpleAggregateFunction(Sum, UInt64),
    dx_30 SimpleAggregateFunction(Sum, UInt64),
    dx_60 SimpleAggregateFunction(Sum, UInt64),
    dx_90 SimpleAggregateFunction(Sum, UInt64),
    dx_180 SimpleAggregateFunction(Sum, UInt64),
    dx_365 SimpleAggregateFunction(Sum, UInt64)
) ENGINE = AggregatingMergeTree()
ORDER BY (
    on_date, store_id, network, campaign_name, campaign_id, ad_name, ad_id
);

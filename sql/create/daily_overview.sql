CREATE TABLE daily_overview
(
    on_date Date,
    store_id Lowcardinality (String),
    network Lowcardinality (String),
    campaign_name Lowcardinality (String),
    campaign_id Lowcardinality (String),
    ad_name Lowcardinality (String),
    ad_id Lowcardinality (String),
    impressions Simpleaggregatefunction (Sum, UInt64),
    clicks Simpleaggregatefunction (Sum, UInt64),
    installs Simpleaggregatefunction (Sum, UInt64),
    revenue Nullable (SimpleAggregateFunction (Sum, Decimal (38, 4))) DEFAULT 0
) ENGINE = AGGREGATINGMERGETREE()
ORDER BY (
    on_date, store_id, network, campaign_name, campaign_id, ad_name, ad_id
);

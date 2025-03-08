CREATE TABLE user_daily_events_attributed
(
  `event_date` Date,
  `event_id` LowCardinality(String),
  `store_id` LowCardinality(String),
  `network` LowCardinality(String),
  `campaign_name` LowCardinality(String),
  `campaign_id` LowCardinality(String),
  `ad_name` LowCardinality(String),
  `ad_id` LowCardinality(String),
  `country_iso` LowCardinality(String),
  `state_iso` LowCardinality(String),
  `city_name` String,
  `event_count` Int32,
  `unique_users` Int32
)
ENGINE = AggregatingMergeTree
ORDER BY (event_date, event_id, store_id, network, campaign_name, campaign_id, ad_name, ad_id, country_iso, state_iso, city_name);

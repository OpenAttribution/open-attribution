CREATE TABLE user_dx_attributed
(
  `install_date` Date,
  `store_id` LowCardinality(String),
  `network` LowCardinality(String),
  `campaign_name` LowCardinality(String),
  `campaign_id` LowCardinality(String),
  `ad_name` LowCardinality(String),
  `ad_id` LowCardinality(String),
  `country_iso` LowCardinality(String),
  `state_iso` LowCardinality(String),
  `city_name` String,
  `dx_1` Int32,
  `dx_2` Int32,
  `dx_3` Int32,
  `dx_4` Int32,
  `dx_5` Int32,
  `dx_6` Int32,
  `dx_7` Int32,
  `dx_15` Int32,
  `dx_30` Int32,
  `dx_60` Int32,
  `dx_90` Int32,
  `dx_180` Int32,
  `dx_365` Int32
)
ENGINE = AggregatingMergeTree
ORDER BY (install_date, store_id, network, campaign_name, campaign_id, ad_name, ad_id, country_iso, state_iso, city_name);

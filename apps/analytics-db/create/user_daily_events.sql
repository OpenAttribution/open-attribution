CREATE TABLE user_daily_events
(
  `event_date` Date,
  `event_id` LowCardinality(String),
  `oa_uid` UUID,
  `event_count` UInt32
)
ENGINE = SummingMergeTree
ORDER BY (event_date, event_id, oa_uid);
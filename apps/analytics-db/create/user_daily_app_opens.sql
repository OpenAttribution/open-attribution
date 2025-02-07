CREATE TABLE user_daily_app_opens
(
  `event_date` Date,
  `oa_uid` UUID,
  `daily_opens` UInt32
)
ENGINE = SummingMergeTree
ORDER BY (event_date, oa_uid);
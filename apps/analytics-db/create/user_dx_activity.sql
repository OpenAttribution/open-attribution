CREATE TABLE user_dx_activity
(
  `install_date` Date,
  `oa_uid` UUID,
  `dx` Int32
)
ENGINE = AggregatingMergeTree
ORDER BY (install_date, oa_uid, dx);


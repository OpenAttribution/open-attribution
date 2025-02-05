CREATE TABLE user_dx_attributed?
(
  `campaign_id` String,
  `campaign_name` String,
  `campaign_sub_id` String,
  `campaign_sub_id_2` String,
  `campaign_sub_id_3` String,
  `campaign_sub_id_4` String,
  `campaign_sub_id_5` String,
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
ORDER BY (install_date, oa_uid, dx);

CREATE TABLE user_dx_attributed?
(
  `install_date` Date, <- installs_base
  
  `campaign_id` String, <- attributed_installs coalesce "Organic"
  `campaign_name` String, <- attributed_installs coalesce "Organic"
  `campaign_sub_id` String, <- attributed_installs coalesce "Organic"
  `campaign_sub_id_2` String, <- attributed_installs coalesce "Organic"
  `campaign_sub_id_3` String, <- attributed_installs coalesce "Organic"
  `campaign_sub_id_4` String, <- attributed_installs coalesce "Organic"
  `campaign_sub_id_5` String, <- attributed_installs coalesce "Organic"
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


Next step: I want to make a new table:

include all the install data

this table can remove the install_date column? Because why have it, go through all the effort of the JOIN and have no data, just need to do the same JOIN again for next table.
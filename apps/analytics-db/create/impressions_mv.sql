CREATE MATERIALIZED VIEW impressions_mv TO impressions AS
SELECT *
FROM impressions_queue;

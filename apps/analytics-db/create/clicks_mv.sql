CREATE MATERIALIZED VIEW clicks_mv TO clicks AS
SELECT *
FROM clicks_queue;

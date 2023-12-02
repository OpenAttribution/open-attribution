CREATE MATERIALIZED VIEW events_mv TO events AS
SELECT *
FROM events_queue;

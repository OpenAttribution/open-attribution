CREATE MATERIALIZED VIEW events_mv TO events AS
SELECT *, _error AS errors
FROM events_queue
SETTINGS
stream_like_engine_allow_direct_select = 1;

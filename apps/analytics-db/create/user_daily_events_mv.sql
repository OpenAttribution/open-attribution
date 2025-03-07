CREATE MATERIALIZED VIEW user_daily_events_mv TO user_daily_events AS
SELECT 
    toDate(event_time) AS event_date,
    event_id,
    oa_uid,
    count() as event_count
FROM events 
GROUP BY event_date, event_id, oa_uid;
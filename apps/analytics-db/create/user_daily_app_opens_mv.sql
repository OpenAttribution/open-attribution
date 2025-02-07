CREATE MATERIALIZED VIEW user_daily_app_opens_mv TO user_daily_app_opens AS
SELECT 
    toDate(event_time) AS event_date,
    oa_uid,
    count() as daily_opens
FROM events 
WHERE event_id = 'app_open'
GROUP BY event_date, oa_uid;
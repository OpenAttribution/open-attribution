CREATE MATERIALIZED VIEW user_dx_activity_mv TO user_dx_activity
AS 
SELECT 
    udo.oa_uid,
    dateDiff('day', ib.install_time, udo.event_date) as dx
FROM user_daily_app_opens udo
    -- ensure we only count opens after install day?
    -- THIS SETS RETENTION AS FLAT BASED ON CALENDAR DATE, not strictly 24hr later
WHERE dateDiff('day', ib.install_time, udo.event_date) >= 1 
GROUP BY 
    udo.oa_uid,
    dx
ORDER BY oa_uid, dx;



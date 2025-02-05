CREATE MATERIALIZED VIEW user_dx_activity_mv 
REFRESH EVERY 1 MINUTE
TO user_dx_activity

AS 
SELECT 
    toDate(ib.install_time) as install_date,
    udo.oa_uid,
    dateDiff('day', ib.install_time, udo.event_date) as dx
FROM user_daily_app_opens udo
JOIN installs_base ib 
    ON udo.oa_uid = ib.oa_uid
    -- ensure we only count opens after install day?
    -- THIS SETS RETENTION AS FLAT BASED ON CALENDAR DATE, not strictly 24hr later
WHERE dateDiff('day', ib.install_time, udo.event_date) >= 1 
GROUP BY 
    install_date,
    udo.oa_uid,
    dx
ORDER BY install_date, oa_uid, dx;



SELECT oa_uid
FROM oa_uid_issuances
WHERE event_uid = :event_uid
LIMIT 1;

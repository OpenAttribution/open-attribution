INSERT INTO oa_uid_issuances (
    event_uid,
    oa_uid,
    store_id,
    ifa
)
VALUES (
    :event_uid,
    :oa_uid,
    :store_id,
    :ifa
)
ON CONFLICT (event_uid) DO NOTHING
RETURNING oa_uid;

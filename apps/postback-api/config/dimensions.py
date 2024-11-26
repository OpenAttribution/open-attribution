"""Set the string names as defined in the database scripts."""

# Link IDs

LINK_STORE_ID = "store_id"
LINK_NETWORK = "network"
LINK_CAMPAIGN = "c"
LINK_CAMPAIGN_ID = "cid"
LINK_AD = "ad"
LINK_AD_ID = "adid"
LINK_IFA = "ifa"
LINK_APP_EVENT_ID = "event_id"
LINK_EVENT_TIME = "event_time"
LINK_UID = "link_uid"

# In App IDs
# sent from the app sdk to the database
APP_EVENT_UID = "event_uid"
APP_EVENT_ID = "event_id"
APP_EVENT_TIME = "event_time"
APP_EVENT_REV = "revenue"
APP_OA_USER_ID = "oa_uid"


# values for kafka -> db columns
DB_STORE_ID = "store_id"
DB_NETWORK = "network"
DB_C = "campaign_name"
DB_C_ID = "campaign_id"
DB_AD_NAME = "ad_name"
DB_AD_ID = "ad_id"
DB_IFA = "ifa"
DB_OA_UID = "oa_uid"
DB_CLIENT_IP = "client_ip"
DB_LINK_UID = "link_uid"
DB_EVENT_UID = "event_uid"
DB_RECEIVED_AT = "received_at"


AD_SHARED_DIMENSIONS = [
    DB_STORE_ID,
    DB_NETWORK,
    DB_C,
    DB_C_ID,
    DB_AD_NAME,
    DB_AD_ID,
    DB_IFA,
    DB_CLIENT_IP,
    DB_LINK_UID,
]

APP_DIMENSIONS = [
    DB_STORE_ID,
    APP_EVENT_ID,
    DB_IFA,
    APP_EVENT_TIME,
    APP_EVENT_REV,
    APP_EVENT_UID,
]

MY_SCHEMAS = {
    "impressions": AD_SHARED_DIMENSIONS,
    "clicks": AD_SHARED_DIMENSIONS,
    "events": APP_DIMENSIONS,
}

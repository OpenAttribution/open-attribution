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


# values for kafka -> druid columns
DB_STORE_ID = "store_id"
DB_NETWORK = "network"
DB_C = "campaign_name"
DB_C_ID = "campaign_id"
DB_AD_NAME = "ad_name"
DB_AD_ID = "ad_id"
DB_IFA = "ifa"
DB_CLIENT_IP = "client_ip"


# In App IDs
APP_EVENT_ID = "event_id"
APP_EVENT_TIME = "event_time"
APP_EVENT_REV = "revenue"


AD_SHARED_DIMENSIONS = [
    DB_STORE_ID,
    DB_NETWORK,
    DB_C,
    DB_C_ID,
    DB_AD_NAME,
    DB_AD_ID,
    DB_IFA,
    DB_CLIENT_IP,
]

APP_DIMENSIONS = [DB_STORE_ID, APP_EVENT_ID, DB_IFA, APP_EVENT_TIME, APP_EVENT_REV]

MY_SCHEMAS = {
    "impressions": AD_SHARED_DIMENSIONS,
    "clicks": AD_SHARED_DIMENSIONS,
    "events": APP_DIMENSIONS,
}

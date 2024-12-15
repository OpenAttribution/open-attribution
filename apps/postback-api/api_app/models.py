"""API models for return types."""

from dataclasses import make_dataclass

from config.dimensions import (
    APP_EVENT_ID,
    APP_EVENT_REV,
    APP_EVENT_TIME,
    DB_AD_ID,
    DB_AD_NAME,
    DB_C,
    DB_C_ID,
    DB_CITY_NAME,
    DB_CLIENT_IP,
    DB_COUNTRY_ISO,
    DB_EVENT_UID,
    DB_IFA,
    DB_LINK_UID,
    DB_NETWORK,
    DB_OA_UID,
    DB_RECEIVED_AT,
    DB_STATE_ISO,
    DB_STORE_ID,
)

# List of field names for your dataclass
impression_click_fields = [
    DB_NETWORK,
    DB_STORE_ID,
    DB_C,
    DB_C_ID,
    DB_AD_NAME,
    DB_AD_ID,
    DB_IFA,
    DB_CLIENT_IP,
    DB_LINK_UID,
    DB_COUNTRY_ISO,
    DB_STATE_ISO,
    DB_CITY_NAME,
    DB_RECEIVED_AT,
]

event_fields = [
    DB_STORE_ID,
    APP_EVENT_ID,
    APP_EVENT_TIME,
    DB_IFA,
    APP_EVENT_REV,
    DB_CLIENT_IP,
    DB_OA_UID,
    DB_EVENT_UID,
    DB_COUNTRY_ISO,
    DB_STATE_ISO,
    DB_CITY_NAME,
    DB_RECEIVED_AT,
]


# Create a dataclass dynamically
ImpressionData = make_dataclass(
    "ImpressionData",  # Name of the dataclass
    [("event_time", str)] + [(field, str) for field in impression_click_fields],
)

ClickData = make_dataclass(
    "ClickData",  # Name of the dataclass
    [("event_time", str)] + [(field, str) for field in impression_click_fields],
)

EventData = make_dataclass(
    "EventData",  # Name of the dataclass
    [(field, str) for field in event_fields],
)

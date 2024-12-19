"""API models for return types."""

from dataclasses import dataclass, make_dataclass

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


@dataclass
class GoogleAssetLink:
    """Represents an asset link in the assetlinks.json file."""

    relation: list[str]
    target: dict[str, str]


@dataclass
class AppleAppSiteAssociationComponent:
    """Represents a component in the apple-app-site-association file."""

    path: str  # Representing the "/" key in the JSON
    id: str  # Representing the "#" key in the JSON
    comment: str | None = None
    exclude: bool | None = None

    def to_dict(self) -> dict:
        """Return the dictionary representation of the AppleAppSiteAssociationComponent."""
        data: dict[str, str | bool | None] = {}
        if self.path is not None:
            data["/"] = self.path
        if self.comment is not None:
            data["comment"] = self.comment
        if self.exclude is not None:
            data["exclude"] = self.exclude
        if self.id is not None:
            data["#"] = self.id
        return data


@dataclass
class Detail:
    """
    Represents a detail in the apple-app-site-association file.

    Works for multiple apps.

    team_app_ids: list[str] are a concatenation of the team ID and the app Bundle.
    """

    team_app_ids: list[str]
    components: list[AppleAppSiteAssociationComponent]

    def to_dict(self) -> dict:
        """Return dictionary representation of Detail section."""
        return {
            "team_app_ids": self.team_app_ids,
            "components": [component.to_dict() for component in self.components],
        }


@dataclass
class Applinks:
    """Represents the applinks section in the apple-app-site-association file."""

    details: list[Detail]

    def to_dict(self) -> dict:
        """Return the dictionary representation of the Applinks."""
        return {"details": [detail.to_dict() for detail in self.details]}


@dataclass
class AppleAASA:
    """Represents the apple-app-site-association file."""

    applinks: Applinks

    def to_dict(self) -> dict:
        """Return the dictionary representation of the AppLinkConfig."""
        return {
            "applinks": self.applinks.to_dict(),
        }

"""Data models for APIs."""

from dataclasses import dataclass


@dataclass
class Network:
    """Network."""

    network: str
    network_name: str


@dataclass
class StoreId:
    """Store ID."""

    store_id: str
    app_name: str


@dataclass
class OverviewData:
    """Main overview for homepage."""

    overview: dict
    networks: list[Network]
    store_ids: list[StoreId]
    dates_overview: dict


@dataclass
class Networks:
    """All networks."""

    networks: dict
    custom_networks: dict


@dataclass
class Apps:
    """All apps."""

    apps: list[dict]


@dataclass
class App:
    """A single app."""

    app: dict


@dataclass
class AppLinks:
    """All app links."""

    links: list[dict]

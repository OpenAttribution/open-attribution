"""Data models for APIs."""

from dataclasses import dataclass


@dataclass
class OverviewData:
    """Main overview for homepage."""

    overview: dict
    dates_overview: dict


@dataclass
class Networks:
    """All networks."""

    networks: dict


@dataclass
class Apps:
    """All apps."""

    apps: dict

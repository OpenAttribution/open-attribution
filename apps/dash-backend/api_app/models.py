"""Data models for APIs."""

from dataclasses import dataclass


@dataclass
class OverviewData:
    """Main overview for homepage."""

    overview: dict
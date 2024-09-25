"""API for returning analytics data for dash."""

from typing import Self

import clickhouse_connect
import pandas as pd
from litestar import Controller, get

from api_app.models import (
    OverviewData,
)
from config import get_logger

logger = get_logger(__name__)

client = clickhouse_connect.create_client(host="clickhouse")


def query_campaign_overview(start_date: str, end_date: str) -> pd.DataFrame:
    """Query the main overview data."""
    query_template = """
    SELECT
        *
    FROM
        daily_overview
    WHERE
        on_date >= %(start_date)s
        AND on_date <= %(end_date)s
    """
    # Execute the query and fetch the data as pandas df
    df = client.query_df(
        query_template,
        parameters={"start_date": start_date, "end_date": end_date},
    )
    return df


class OverviewController(Controller):
    """Controller holding all API endpoints for an app."""

    path = "/api/overview"

    @get(path="/")
    async def get_overview(self: Self, start_date: str, end_date: str) -> OverviewData:
        """
        Handle GET request for a list of apps.

        Args:
        ----
            start_date: str, like 2024-09-25
            end_date: str, like 2024-10-31

        Returns:
        -------
            A table with the overview breakdown for homepage

        """
        logger.info(f"{self.path} overview load {start_date=} {end_date=}")
        home_df = query_campaign_overview(start_date=start_date, end_date=end_date)

        home_dict = home_df.to_dict(orient="records")

        myresp = OverviewData(overview=home_dict)

        logger.info(f"{self.path} return")
        return myresp

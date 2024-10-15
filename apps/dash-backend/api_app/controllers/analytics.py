"""API for returning analytics data for dash."""

from typing import Self

import clickhouse_connect
import pandas as pd
from config import get_logger
from dbcon.queries import query_apps, query_networks
from litestar import Controller, get

from api_app.models import (
    OverviewData,
)

logger = get_logger(__name__)

# Seems like this needs to be localhost, not docker specific clickhouse?
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
            A table with the overview breakdown for homepage from clickhouse

        """
        logger.info(f"{self.path} overview load {start_date=} {end_date=}")
        df = query_campaign_overview(start_date=start_date, end_date=end_date)

        apps_df = query_apps().rename(columns={"name": "app_name"})
        networks_df = query_networks().rename(columns={"name": "network_name"})

        df = df.merge(apps_df, left_on="store_id", right_on="store_id", how="outer")
        df = df.merge(
            networks_df, left_on="network", right_on="postback_id", how="outer",
        )

        df.loc[df["app_name"].isna(), "app_name"] = df.loc[
            df["app_name"].isna(), "store_id",
        ]
        df.loc[df["network_name"].isna(), "network_name"] = df.loc[
            df["network_name"].isna(), "network",
        ]

        df["revenue"] = df["revenue"].astype(float)

        dates_home_df = (
            df.groupby(
                by=[
                    "on_date",
                    "store_id",
                    "network",
                    "network_name",
                    "app_name",
                    "campaign_name",
                    "campaign_id",
                ],
            )[["impressions", "clicks", "installs", "revenue"]]
            .sum()
            .reset_index()
        )
        home_df = (
            df.groupby(
                [
                    "store_id",
                    "network",
                    "network_name",
                    "app_name",
                    "campaign_name",
                    "campaign_id",
                    "ad_name",
                    "ad_id",
                ],
            )[["impressions", "clicks", "installs", "revenue"]]
            .sum()
            .reset_index()
        )

        home_dict = home_df.to_dict(orient="records")
        dates_home_dict = dates_home_df.to_dict(orient="records")

        myresp = OverviewData(overview=home_dict, dates_overview=dates_home_dict)

        logger.info(f"{self.path} return rows {home_df.shape}")
        return myresp

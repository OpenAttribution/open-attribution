"""API for returning analytics data for dash."""

import sys
from typing import Self

import clickhouse_connect
import pandas as pd
from config import get_logger
from dbcon.queries import query_apps, query_networks
from litestar import Controller, get
from litestar.exceptions import HTTPException

from api_app.models import (
    OverviewData,
)

logger = get_logger(__name__)

# When testing locally, this needs to be localhost
# When running in docker, it needs to be clickhouse
if hasattr(sys, "ps1"):
    client = clickhouse_connect.create_client(host="localhost")
else:
    client = clickhouse_connect.create_client(host="clickhouse")



def query_campaign_overview(start_date: str, end_date: str) -> pd.DataFrame:
    """Query the main overview data."""
    query_template = """SELECT
                        on_date,
                        network,
                        store_id,
                        campaign_name,
                        campaign_id,
                        country_iso,
                        ad_name,
                        ad_id,
                        sum(impressions) as impressions,
                        sum(clicks) as clicks,
                        sum(installs) as installs,
                        sum(revenue) as revenue
                    FROM
                        daily_overview
                    WHERE
                        on_date BETWEEN toDate(%(start_date)s) AND toDate(%(end_date)s)
                    GROUP BY
                        on_date,
                        network,
                        store_id,
                        campaign_name,
                        campaign_id,
                        country_iso,
                        ad_name,
                        ad_id
                    ORDER BY
                        on_date
                    WITH FILL
                    FROM toDate(%(start_date)s) TO toDate(%(end_date)s) STEP INTERVAL 1 DAY
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

        if start_date == "null" or end_date == "null":
            raise HTTPException(status_code=404, detail="Date range not specified")

        df = query_campaign_overview(start_date=start_date, end_date=end_date)


        apps_df = query_apps().rename(columns={"name": "app_name"})
        networks_df = query_networks().rename(columns={"name": "network_name"})


        df = df.merge(apps_df, left_on="store_id", right_on="store_id", how="left")
        df = df.merge(
            networks_df, left_on="network", right_on="postback_id", how="left",
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
                    "country_iso",
                ],
                dropna=False,
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
                    "country_iso",
                    "ad_name",
                    "ad_id",
                ],
                dropna=False,
            )[["impressions", "clicks", "installs", "revenue"]]
            .sum()
            .reset_index()
        )

        home_dict = home_df.to_dict(orient="records")
        dates_home_df["on_date"] = dates_home_df["on_date"].dt.date
        dates_home_dict = dates_home_df.to_dict(orient="records")

        logger.info(f"PLOT DF {len(dates_home_dict)=}")

        found_networks = home_df[["network", "network_name"]].drop_duplicates().to_dict(orient="records")
        found_store_ids = home_df[["store_id", "app_name"]].drop_duplicates().to_dict(orient="records")

        logger.info(f"{self.path} overview load {start_date=} {end_date=} {found_networks=} {found_store_ids=}")

        myresp = OverviewData(overview=home_dict, dates_overview=dates_home_dict, networks=found_networks, store_ids=found_store_ids)

        logger.info(f"{self.path} return rows {home_df.shape}")
        return myresp

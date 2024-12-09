"""API for returning analytics data for dash."""

from enum import Enum
from typing import Self

import dbcon
import dbcon.queries
from config import get_logger
from litestar import Controller, get

from dash_api.models import AppLinks

logger = get_logger(__name__)


class LinkController(Controller):
    """Controll all ad apps."""

    path = "/api/links"

    @get(path="/")
    async def links(self: Self) -> AppLinks:
        """
        Handle GET request for a list of links.

        Returns
        -------
            Data for a list of links

        """
        logger.info(f"{self.path} links load")
        df = dbcon.queries.query_app_links()
        links_dict = df.to_dict(orient="records")
        myresp = AppLinks(links=links_dict)
        logger.info(f"{self.path} return {links_dict=}")
        return myresp

    # @post(path="/{app_id:int}/links")
    # async def add_app_link(
    #     self: Self,
    #     app_id: int,
    #     share_slug: str,
    #     network_id: int,
    #     campaign_name: str,
    #     ad_name: str,
    # ) -> None:
    #     """Create an app link."""
    #     logger.info(
    #         f"{self.path} apps add {app_id=} {share_slug=} {network_id=} {campaign_name=}",
    #     )

    #     dbcon.queries.insert_app_link(
    #         share_slug=share_slug,
    #         network_id=network_id,
    #         campaign_name=campaign_name,
    #         ad_name=ad_name,
    #         app_id=app_id,
    #     )

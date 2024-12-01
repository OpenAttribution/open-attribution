"""API for returning analytics data for dash."""

from typing import Self

import dbcon
import dbcon.queries
from config import get_logger
from litestar import Controller, delete, get, post

from dash_api.models import Networks

logger = get_logger(__name__)


class NetworkController(Controller):
    """Controll all ad networks."""

    path = "/api/networks"

    @get(path="/")
    async def networks(self: Self) -> Networks:
        """
        Handle GET request for a list of networks.

        Returns
        -------
            A table with the networks from admin-db

        """
        logger.info(f"{self.path} networks load")
        nets_df = dbcon.queries.query_networks()
        networks_dict = nets_df.to_dict(orient="records")
        myresp = Networks(networks=networks_dict)
        logger.info(f"{self.path} return rows {nets_df.shape}")
        return myresp

    @post(path="/{network_name:str}")
    async def add_custom_networks(self: Self, network_name: str) -> None:
        """Create a custom network."""
        logger.info(f"{self.path} networks add {network_name=}")
        dbcon.queries.insert_network(network_name)

    @delete(path="/{network_id:int}")
    async def delete_custom_networks(self: Self, network_id: int) -> None:
        """Handle DELETE request for a list of networks."""
        logger.info(f"{self.path} networks DELETE {network_id=}")
        dbcon.queries.delete_network(network_id)

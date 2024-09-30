"""API for returning analytics data for dash."""

from typing import Self

import dbcon
import dbcon.queries
from config import get_logger
from litestar import Controller, get

from api_app.models import Networks

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
            A table with the overview breakdown for homepage from clickhouse

        """
        logger.info(f"{self.path} networks load")
        nets_df = dbcon.queries.query_networks()
        networks_dict = nets_df.to_dict(orient="records")
        myresp = Networks(networks=networks_dict)
        logger.info(f"{self.path} return rows {nets_df.shape}")
        return myresp

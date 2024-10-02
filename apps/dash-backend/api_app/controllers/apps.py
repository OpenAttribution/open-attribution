"""API for returning analytics data for dash."""

from typing import Self

import dbcon
import dbcon.queries
from config import get_logger
from litestar import Controller, delete, get, post

from api_app.models import Apps

logger = get_logger(__name__)


class AppController(Controller):
    """Controll all ad apps."""

    path = "/api/apps"

    @get(path="/")
    async def apps(self: Self) -> Apps:
        """
        Handle GET request for a list of apps.

        Returns
        -------
            A table with the apps from admin-db

        """
        logger.info(f"{self.path} apps load")
        nets_df = dbcon.queries.query_apps()
        apps_dict = nets_df.to_dict(orient="records")
        myresp = Apps(apps=apps_dict)
        logger.info(f"{self.path} return rows {nets_df.shape}")
        return myresp

    @post(path="/{store_id:str}")
    async def add_app(self: Self, store_id: str, app_name: str, store: int) -> None:
        """Create a custom app."""
        logger.info(f"{self.path} apps add {app_name=}")
        dbcon.queries.insert_app(app_name=app_name, store_id=store_id, store=store)

    @delete(path="/{app_id:int}")
    async def delete_app(self: Self, app_id: int) -> None:
        """Handle DELETE request for a list of apps."""
        logger.info(f"{self.path} apps DELETE {app_id=}")
        dbcon.queries.delete_app(app_id)

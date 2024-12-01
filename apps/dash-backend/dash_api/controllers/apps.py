"""API for returning analytics data for dash."""

from enum import Enum
from typing import Self

import dbcon
import dbcon.queries
from config import get_logger
from litestar import Controller, delete, get, post

from dash_api.models import Apps

logger = get_logger(__name__)


class StoreEnum(str, Enum):
    """Enum for receivable store names."""

    IOS = "ios"
    ANDROID = "android"


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
        apps_df = dbcon.queries.query_apps()
        apps_dict = apps_df.to_dict(orient="records")
        myresp = Apps(apps=apps_dict)
        logger.info(f"{self.path} return rows {apps_df.shape}")
        return myresp

    @post(path="/{store_id:str}")
    async def add_app(
        self: Self,
        store_id: str,
        app_name: str,
        store: StoreEnum,
    ) -> None:
        """Create an app."""
        logger.info(f"{self.path} apps add {app_name=}")

        if store == StoreEnum.ANDROID:
            store_db_id = 1
        if store == StoreEnum.IOS:
            store_db_id = 2

        dbcon.queries.insert_app(
            app_name=app_name,
            store_id=store_id,
            store=store_db_id,
        )

    @delete(path="/{app_id:int}")
    async def delete_app(self: Self, app_id: int) -> None:
        """Handle DELETE request for a list of apps."""
        logger.info(f"{self.path} apps DELETE {app_id=}")
        dbcon.queries.delete_app(app_id)

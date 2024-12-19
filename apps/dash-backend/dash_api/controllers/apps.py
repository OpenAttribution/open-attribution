"""API for returning analytics data for dash."""

from enum import Enum
from typing import Self

import dbcon
import dbcon.queries
from config import get_logger
from litestar import Controller, delete, get, post

from dash_api.models import App, AppData, Apps

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

    @get(path="/{store_id:str}")
    async def app(self: Self, store_id: str) -> App:
        """
        Handle GET request for a single app.

        Returns
        -------
            Data for a single app

        """
        logger.info(f"{self.path} apps load")
        app_df = dbcon.queries.query_apps(store_id)
        app_dict = app_df.to_dict(orient="records")[0]
        myresp = App(app=app_dict)
        logger.info(f"{self.path} return {app_dict=}")
        return myresp

    @post(path="/{store_id:str}")
    async def add_app(
        self: Self,
        store_id: str,
        data: AppData,
    ) -> None:
        """
        Create an app.

        Request body should contain:
        {
            "app_name": string,
            "store": string,
            "bundle_id": string | null,
            "apple_team_id": string | null,
            "google_sha256_fingerprints": list[string] | null,
        }
        """
        app_name = data.app_name
        bundle_id = data.bundle_id
        apple_team_id = data.apple_team_id
        google_sha256_fingerprints = data.google_sha256_fingerprints

        logger.info(f"{self.path} apps add {app_name=}")

        if data.store == StoreEnum.ANDROID:
            store_db_id = 1
        if data.store == StoreEnum.IOS:
            store_db_id = 2

        if google_sha256_fingerprints:
            google_sha256_fingerprints = [
                x.replace(":", "") for x in google_sha256_fingerprints
            ]

        dbcon.queries.insert_app(
            app_name=app_name,
            store_id=store_id,
            store=store_db_id,
            bundle_id=bundle_id,
            apple_team_id=apple_team_id,
            google_sha256_fingerprints=google_sha256_fingerprints,
        )

    @delete(path="/{app_id:int}")
    async def delete_app(self: Self, app_id: int) -> None:
        """Handle DELETE request for a list of apps."""
        logger.info(f"{self.path} apps DELETE {app_id=}")
        dbcon.queries.delete_app(app_id)

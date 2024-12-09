"""API for returning analytics data for dash."""

from enum import Enum
from typing import Self

import dbcon
import dbcon.queries
from config import get_logger
from litestar import Controller, delete, get, post

from dash_api.models import App, AppLinks, Apps

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

    @get(path="/{app_id:int}/links")
    async def app_links(self: Self, app_id: int) -> AppLinks:
        """
        Handle GET request for a single app links.

        Returns
        -------
            Data for a single app links

        """
        logger.info(f"{self.path} apps load")
        df = dbcon.queries.query_app_links(app_id)
        links_dict = df.to_dict(orient="records")
        myresp = AppLinks(links=links_dict)
        logger.info(f"{self.path} return {links_dict=}")
        return myresp

    @post(path="/{app_id:int}/links")
    async def add_app_link(
        self: Self,
        app_id: int,
        share_slug: str,
        network_id: int,
        campaign_name: str,
        ad_name: str,
    ) -> None:
        """Create an app link."""
        logger.info(
            f"{self.path} apps add {app_id=} {share_slug=} {network_id=} {campaign_name=}",
        )

        dbcon.queries.insert_app_link(
            share_slug=share_slug,
            network_id=network_id,
            campaign_name=campaign_name,
            ad_name=ad_name,
            app_id=app_id,
        )

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

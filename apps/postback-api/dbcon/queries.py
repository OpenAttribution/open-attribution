"""Query database for backend API."""

import pathlib
from typing import cast

import pandas as pd
from api_app.models import AppStores
from config import MODULE_DIR, get_logger
from litestar.stores.memory import MemoryStore
from sqlalchemy import Engine, text

from dbcon.connections import get_db_connection

logger = get_logger(__name__)


SQL_DIR = pathlib.Path(MODULE_DIR, "dbcon/sql/")


def load_sql_file(file_name: str) -> str:
    """Load local SQL file based on file name."""
    file_path = pathlib.Path(SQL_DIR, file_name)
    with file_path.open() as file:
        mytxt: str = text(file.read())
        return mytxt


QUERY_APPS = load_sql_file("apps.sql")
QUERY_APP_LINKS = load_sql_file(
    "app_links.sql",
)


async def get_app_links() -> dict[str, dict[str, str]]:
    """Get all app links."""
    logger.info("Query all app links.")
    df = pd.read_sql(
        QUERY_APP_LINKS,
        con=DBCON.engine,
    )
    df["web_redirect"] = "https://" + df["web_landing_page"]
    df["google_redirect"] = (
        "https://play.google.com/store/apps/details?id=" + df["google_store_id"]
    )
    df["apple_redirect"] = "https://apps.apple.com/-/app/-/id" + df["apple_store_id"]
    # Add the android market uri
    # url= maps to the app link verified domain url to open app when installed
    df["android_market_uri"] = (
        "market://details?id=" + df["google_store_id"] + "&url=" + df["domain_url"]
    )
    if df.empty:
        return {}
    df = df.where(pd.notna(df), None)
    app_links = df.set_index("share_slug").to_dict(
        orient="index",
    )
    return app_links


async def get_apps() -> pd.DataFrame:
    """Get all apps."""
    logger.info("Query all apps.")
    df = pd.read_sql(
        QUERY_APPS,
        con=DBCON.engine,
    )
    return df


logger.info("set db engine")
DBCON = get_db_connection()
DBCON.set_engine()

if DBCON.engine is None:
    msg = "DBCON.engine is None"
    logger.error(msg)
    raise ValueError(msg)


ENGINE = cast(Engine, DBCON.engine)

STORE = MemoryStore()


async def update_app_links_store() -> None:
    """Update the app links store."""
    app_links = await get_app_links()
    await STORE.set("app_links", app_links)
    logger.info(f"app_links updated num: {len(app_links)}")


async def update_apps_well_known_store() -> None:
    """Update the apps well-known store."""
    apps = await get_apps()
    if apps.empty:
        logger.warning("No apps found")
        await STORE.set("android_apps", {})
        await STORE.set("ios_apps", {})
        return

    android_apps = {}
    for _, app in apps[apps["store"] == AppStores.ANDROID.db_id].iterrows():
        package_name = app.store_id
        google_sha256_cert_fingerprints = app.google_sha256_fingerprints
        android_apps[package_name] = {
            "sha256_cert_fingerprints": google_sha256_cert_fingerprints,
        }
    await STORE.set("android_apps", android_apps)

    ios_apps = {}
    for _, app in apps[apps["store"] == AppStores.IOS.db_id].iterrows():
        store_id = app.store_id
        bundle_id = app.bundle_id
        apple_team_id = app.apple_team_id
        ios_apps[store_id] = {
            "bundle_id": bundle_id,
            "apple_team_id": apple_team_id,
        }
    await STORE.set("ios_apps", ios_apps)
    logger.info(f"apps updated num: {apps.shape[0]}")

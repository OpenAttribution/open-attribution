"""Query database for backend API."""

import pathlib
from typing import cast

import pandas as pd
from config import MODULE_DIR, get_logger
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


QUERY_APP_LINKS = load_sql_file(
    "app_links.sql",
)


def get_app_links() -> dict[str, dict[str, str]]:
    """Get all app links."""
    logger.info("Query all app links.")
    df = pd.read_sql(
        QUERY_APP_LINKS,
        con=DBCON.engine,
    )
    df["google_redirect"] = (
        "https://play.google.com/store/apps/details?id=" + df["google_store_id"]
    )
    df["apple_redirect"] = "https://apps.apple.com/-/app/-/id" + df["apple_store_id"]
    if df.empty:
        return {}
    app_links = df.set_index("share_slug").to_dict(orient="index")
    return app_links


logger.info("set db engine")
DBCON = get_db_connection()
DBCON.set_engine()

if DBCON.engine is None:
    msg = "DBCON.engine is None"
    logger.error(msg)
    raise ValueError(msg)

ENGINE = cast(Engine, DBCON.engine)

APP_LINKS_DF = get_app_links()

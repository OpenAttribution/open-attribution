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


QUERY_NETWORKS = load_sql_file(
    "networks.sql",
)
INSERT_NETWORK = load_sql_file(
    "insert_network.sql",
)
DELETE_NETWORK = load_sql_file(
    "delete_network.sql",
)

QUERY_APPS = load_sql_file(
    "apps.sql",
)
INSERT_APP = load_sql_file(
    "insert_app.sql",
)
DELETE_APP = load_sql_file(
    "delete_app.sql",
)


def query_networks() -> pd.DataFrame:
    """Get all networks."""
    logger.info("Query all networks.")
    df = pd.read_sql(
        QUERY_NETWORKS,
        con=DBCON.engine,
    )
    return df


def insert_network(network_name: str) -> None:
    """Insert a new network."""
    logger.info(f"Inserting new network: {network_name}")

    with ENGINE.connect() as connection:
        connection.execute(
            INSERT_NETWORK,
            {"network_name": network_name, "status": "active"},
        )
        connection.commit()


def delete_network(network_id: int) -> None:
    """Delete custom network."""
    logger.info(f"Delete network: {network_id}")

    with ENGINE.connect() as connection:
        connection.execute(DELETE_NETWORK, {"network_id": network_id})
        connection.commit()


def query_apps() -> pd.DataFrame:
    """Get all networks."""
    logger.info("Query all apps.")
    df = pd.read_sql(
        QUERY_APPS,
        con=ENGINE,
    )
    return df


def insert_app(app_name: str, store_id: str, store: int) -> None:
    """Insert a new network."""
    logger.info(f"Inserting new app: {app_name}")

    with ENGINE.connect() as connection:
        connection.execute(
            INSERT_APP,
            {"app_name": app_name, "store_id": store_id, "store": store},
        )
        connection.commit()


def delete_app(app_id: int) -> None:
    """Delete custom network."""
    logger.info(f"Delete app: {app_id}")

    with ENGINE.connect() as connection:
        connection.execute(DELETE_NETWORK, {"app_id": app_id})
        connection.commit()


logger.info("set db engine")
DBCON = get_db_connection("admin-db")
DBCON.set_engine()

if DBCON.engine is None:
    raise ValueError("DBCON.engine is None")

assert DBCON.engine is not None, "DBCON.engine is None"
ENGINE = cast(Engine, DBCON.engine)

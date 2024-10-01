"""Query database for backend API."""

import pathlib

import pandas as pd
from config import MODULE_DIR, get_logger
from sqlalchemy import text

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


def query_networks() -> pd.DataFrame:
    """Get all networks."""
    logger.info("Query all networks.")
    df = pd.read_sql(
        QUERY_NETWORKS,
        con=DBCON.engine,
    )
    return df


def insert_network(network_name: str) -> None:
    """Get all networks."""
    logger.info(f"Insert new {network_name=}.")
    pd.read_sql(
        INSERT_NETWORK,
        con=DBCON.engine,
        params={"network_name": network_name},
    )


logger.info("set db engine")
DBCON = get_db_connection("admin-db")
DBCON.set_engine()

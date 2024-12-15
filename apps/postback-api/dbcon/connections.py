"""Create SQLAlchemy database connection engine."""

import sys
from typing import Self

from config import POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER, get_logger
from sqlalchemy import Engine, create_engine

logger = get_logger(__name__)

# When testing locally, this needs to be localhost
# When running in docker, it needs to be clickhouse
DB_HOST = "localhost" if hasattr(sys, "ps1") else "admin-db"


class PostgresCon:
    """
    Class for managing the connection to postgres.

    Parameters
    ----------
    db_name: str, name of the database
    db_host: str, hostname of the database server
    db_port: str, port number for the database connection
    db_user: str, username for database authentication
    db_password: str, password for database authentication

    """

    engine: Engine | None = None
    db_name: str | None = None
    db_pass: str | None = None
    db_uri: str | None = None
    db_user: str | None = None
    db_ip: str | None = None
    db_port: str | None = None

    def __init__(
        self: Self,
        db_name: str,
        db_host: str,
        db_port: str,
        db_user: str,
        db_password: str,
    ) -> None:
        """Initialize connection with ports and dbname."""
        self.db_name = db_name
        self.db_ip = db_host
        self.db_port = db_port
        self.db_user = db_user
        self.db_pass = db_password
        logger.info("Auth data loaded")

    def set_engine(self: Self) -> None:
        """Set postgresql engine."""
        try:
            self.db_uri = f"postgresql://{self.db_user}:{self.db_pass}"
            self.db_uri += f"@{self.db_ip}:{self.db_port}/{self.db_name}"
            self.engine = create_engine(
                self.db_uri,
                connect_args={
                    "connect_timeout": 10,
                    "application_name": "postback-api",
                },
            )
            logger.info(f"Created PostgreSQL Engine {self.db_name}")
        except Exception as error:
            msg = (
                f"PostgresCon failed to connect to {self.db_name}@{self.db_ip} {error=}"
            )
            logger.exception(msg)
            self.db_name = None


def get_db_connection() -> PostgresCon:
    """
    Return PostgresCon class.

    to use class run server.set_engine()

    ====
    Parameters
       server_name: str String of server name for parsing config file
    """
    db_host = DB_HOST
    db_local_port = "5432"

    postgres_con = PostgresCon(
        POSTGRES_DB, db_host, db_local_port, POSTGRES_USER, POSTGRES_PASSWORD,
    )
    return postgres_con

"""Create SQLAlchemy database connection engine."""

from typing import Self

from config import get_logger
from sqlalchemy import Engine, create_engine

logger = get_logger(__name__)


class PostgresCon:
    """
    Class for managing the connection to postgres.

    Parameters
    ----------
        my_db: String, passed on init, string name of db
        my_env: String, passed on init, string name of env, 'staging' or 'prod'

    """

    engine: None | Engine = None
    db_name = None
    db_pass = None
    db_uri = None
    db_user = None

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
            self.engine: Engine = create_engine(
                self.db_uri,
                connect_args={
                    "connect_timeout": 10,
                    "application_name": "dash-backend",
                },
            )
            logger.info(f"Created PostgreSQL Engine {self.db_name}")
        except Exception as error:
            msg = (
                f"PostgresCon failed to connect to {self.db_name}@{self.db_ip} {error=}"
            )
            logger.exception(msg)
            self.db_name = None


def get_db_connection(db_name: str) -> PostgresCon:
    """
    Return PostgresCon class.

    to use class run server.set_engine()

    ====
    Parameters
       server_name: str String of server name for parsing config file
    """
    db_name = "admin_db"
    db_host = "admin-db"
    db_local_port = "5432"
    db_user = "postgres"
    db_password = "example"
    postgres_con = PostgresCon(db_name, db_host, db_local_port, db_user, db_password)
    return postgres_con

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
DELETE_CLIENT_DOMAIN = load_sql_file(
    "delete_client_domain.sql",
)

QUERY_APPS = load_sql_file(
    "apps.sql",
)
QUERY_APP = load_sql_file(
    "app.sql",
)
QUERY_APP_LINKS = load_sql_file(
    "app_links.sql",
)
QUERY_CLIENT_DOMAINS = load_sql_file(
    "client_domains.sql",
)
INSERT_CLIENT_DOMAINS = load_sql_file(
    "insert_client_domains.sql",
)

INSERT_APP = load_sql_file(
    "insert_app.sql",
)
DELETE_APP = load_sql_file(
    "delete_app.sql",
)

DELETE_APP_LINK = load_sql_file(
    "delete_app_link.sql",
)

INSERT_APP_LINK = load_sql_file(
    "insert_app_link.sql",
)


def query_networks() -> pd.DataFrame:
    """Get all networks."""
    logger.info("Query all networks.")
    df = pd.read_sql(
        QUERY_NETWORKS,
        con=DBCON.engine,
    )
    return df


def query_app_links() -> pd.DataFrame:
    """Get all apps links."""
    logger.info("Query all apps links.")
    df = pd.read_sql(
        QUERY_APP_LINKS,
        con=DBCON.engine,
    )
    df["full_url"] = df["domain_url"] + "/" + df["share_slug"]
    return df


def query_client_domains() -> pd.DataFrame:
    """Get all client domains."""
    logger.info("Query all client domains.")
    df = pd.read_sql(
        QUERY_CLIENT_DOMAINS,
        con=DBCON.engine,
    )
    return df


def insert_client_domains(domain_url: str) -> None:
    """Insert a new client domain."""
    logger.info(f"Inserting new client domain: {domain_url}")

    with ENGINE.connect() as connection:
        connection.execute(INSERT_CLIENT_DOMAINS, {"domain_url": domain_url})
        connection.commit()


def insert_custom_network(network_name: str, postback_id: str) -> None:
    """Insert a new network."""
    logger.info(f"Inserting new network: {network_name} {postback_id=}")

    with ENGINE.connect() as connection:
        connection.execute(
            INSERT_NETWORK,
            {
                "network_name": network_name,
                "status": "active",
                "postback_id": postback_id,
                "is_custom": True,
            },
        )
        connection.commit()


def delete_network(network_id: int) -> None:
    """Delete custom network."""
    logger.info(f"Delete network: {network_id}")

    with ENGINE.connect() as connection:
        connection.execute(DELETE_NETWORK, {"network_id": network_id})
        connection.commit()


def query_apps(store_id: str | None = None) -> pd.DataFrame:
    """Get all apps or a single app."""
    logger.info(f"Query {'all' if store_id is None else f'app: {store_id}'} apps.")

    if store_id is None:
        df = pd.read_sql(
            QUERY_APPS,
            con=ENGINE,
        )
    else:
        df = pd.read_sql(
            QUERY_APP,
            params={"store_id": store_id},
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
    """Delete app."""
    logger.info(f"Delete app: {app_id}")

    with ENGINE.connect() as connection:
        connection.execute(DELETE_APP, {"app_id": app_id})
        connection.commit()


def delete_app_link(link_id: int) -> None:
    """Delete app link."""
    logger.info(f"Delete app link: {link_id}")

    with ENGINE.connect() as connection:
        connection.execute(DELETE_APP_LINK, {"link_id": link_id})
        connection.commit()


def delete_client_domain(domain_id: int) -> None:
    """Delete custom network."""
    logger.info(f"Delete client domain: {domain_id}")

    with ENGINE.connect() as connection:
        connection.execute(DELETE_CLIENT_DOMAIN, {"id": domain_id})
        connection.commit()


def insert_app_link(
    domain_id: int,
    google_app_id: int | None,
    apple_app_id: int | None,
    share_slug: str,
    network_id: int,
    campaign_name: str,
    ad_name: str | None,
    web_landing_page: str,
) -> None:
    """Insert a new app link."""
    logger.info(
        f"Inserting new app link: {share_slug} {network_id} {campaign_name} {ad_name} {domain_id} {google_app_id} {apple_app_id}",
    )

    with ENGINE.connect() as connection:
        connection.execute(
            INSERT_APP_LINK,
            {
                "domain_id": domain_id,
                "google_app_id": google_app_id,
                "apple_app_id": apple_app_id,
                "share_slug": share_slug,
                "network_id": network_id,
                "campaign_name": campaign_name,
                "ad_name": ad_name,
                "web_landing_page": web_landing_page,
            },
        )
        connection.commit()


logger.info("set db engine")
DBCON = get_db_connection()
DBCON.set_engine()

if DBCON.engine is None:
    msg = "DBCON.engine is None"
    logger.error(msg)
    raise ValueError(msg)

ENGINE = cast(Engine, DBCON.engine)

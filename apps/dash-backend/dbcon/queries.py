"""Query database for backend API."""

import datetime
import pathlib

import numpy as np
import pandas as pd
from sqlalchemy import text

from config import MODULE_DIR, get_logger
from dbcon.connections import get_db_connection

logger = get_logger(__name__)


SQL_DIR = pathlib.Path(MODULE_DIR, "dbcon/sql/")


def load_sql_file(file_name: str) -> str:
    """Load local SQL file based on file name."""
    file_path = pathlib.Path(SQL_DIR, file_name)
    with file_path.open() as file:
        return text(file.read())


QUERY_CATEGORY_TOP_APPS_BY_INSTALLS = load_sql_file(
    "query_category_top_apps_by_installs.sql",
)
QUERY_RANKS_FOR_APP = load_sql_file("query_ranks_for_app.sql")
QUERY_MOST_RECENT_TOP_RANKS = load_sql_file("query_most_recent_top_ranks.sql")
QUERY_HISTORY_TOP_RANKS = load_sql_file("query_history_top_ranks.sql")
QUERY_APPSTORE_CATEGORIES = load_sql_file("query_appstore_categories.sql")
QUERY_SEARCH_APPS = load_sql_file("query_search_apps.sql")
QUERY_SEARCH_DEVS = load_sql_file("query_search_devs.sql")
QUERY_SINGLE_DEVELOPER = load_sql_file("query_single_developer.sql")
QUERY_SINGLE_DEVELOPER_ADSTXT = load_sql_file("query_single_developer_adstxt.sql")
QUERY_APP_HISTORY = load_sql_file("query_app_history.sql")
QUERY_SINGLE_APP = load_sql_file("query_single_app.sql")
QUERY_APP_PACKAGE_DETAILS = load_sql_file("query_app_package_details.sql")
QUERY_STORE_COLLECTION_CATEGORY_MAP = load_sql_file(
    "query_store_collection_category_map.sql",
)
QUERY_TOP_COMPANIES_MONTH = load_sql_file("query_top_companies_month.sql")
QUERY_TOP_PARENT_COMPANIES_MONTH = load_sql_file("query_top_companies_month_parent.sql")
QUERY_COMPANY_APPS = load_sql_file("query_company_apps.sql")
QUERY_PARENT_COMPANY_APPS = load_sql_file("query_parent_company_apps.sql")


def get_recent_apps(collection: str, limit: int = 20) -> pd.DataFrame:
    """Get app collections by time."""
    logger.info(f"Query app_store for recent apps {collection=}")
    if collection == "new_weekly":
        table_name = "apps_new_weekly"
    elif collection == "new_monthly":
        table_name = "apps_new_monthly"
    elif collection == "new_yearly":
        table_name = "apps_new_yearly"
    elif collection == "top":
        table_name = "top_categories"
    else:
        table_name = "apps_new_weekly"
    cols = [
        "name",
        "store",
        "mapped_category",
        "store_id",
        "installs",
        "review_count",
        "rating_count",
        "rating",
        "icon_url_512",
        "featured_image_url",
        "phone_image_url_1",
        "tablet_image_url_1",
    ]
    my_cols = ", ".join(cols)
    sel_query = f"""WITH NumberedRows AS (
                    SELECT 
                        {my_cols},
                        ROW_NUMBER() OVER (PARTITION BY store, mapped_category
                    ORDER BY 
                        CASE WHEN store = 1 THEN installs ELSE rating_count END DESC NULLS LAST
                ) AS rn
                FROM {table_name}
            )
            SELECT 
                {my_cols}
            FROM NumberedRows
            WHERE rn <= {limit}
            ;
            """  # noqa: S608 worried about SQL injection but all data is set internal
    df = pd.read_sql(sel_query, con=DBCON.engine)
    groups = df.groupby("store")
    for _store, group in groups:
        overall = group.sort_values(["installs", "rating_count"], ascending=False).head(
            limit,
        )
        overall["mapped_category"] = "overall"
        df = pd.concat([df, overall], axis=0)
    df = clean_app_df(df)
    return df


def get_appstore_categories() -> pd.DataFrame:
    """Get categories for both appstores."""
    df = pd.read_sql(QUERY_APPSTORE_CATEGORIES, DBCON.engine)
    df["store"] = df["store"].replace({1: "android", 2: "ios"})
    df = pd.pivot_table(
        data=df,
        index="category",
        values="app_count",
        columns="store",
        fill_value=0,
    ).reset_index()
    df["total_apps"] = df["android"] + df["ios"]
    df = df.sort_values("total_apps", ascending=False)
    return df


def get_ranks_for_app(store_id: str, days: int = 30) -> pd.DataFrame:
    """Get appstore ranks for a specific app."""
    start_date = (
        datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=days)
    ).strftime("%Y-%m-%d")
    df = pd.read_sql(
        QUERY_RANKS_FOR_APP,
        con=DBCON.engine,
        params={"store_id": store_id, "start_date": start_date},
    )
    return df


def get_most_recent_top_ranks(
    store: int,
    collection_id: int,
    category_id: int,
    limit: int = 25,
) -> pd.DataFrame:
    """Get the latest top ranks for a category."""
    df = pd.read_sql(
        QUERY_MOST_RECENT_TOP_RANKS,
        con=DBCON.engine,
        params={
            "store": store,
            "collection_id": collection_id,
            "category_id": category_id,
            "mylimit": limit,
        },
    )
    return df


def get_history_top_ranks(
    store: int,
    collection_id: int,
    category_id: int,
    limit: int = 25,
    days: int = 30,
) -> pd.DataFrame:
    """Get appstore rank history for plotting."""
    start_date = (
        datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=days)
    ).strftime("%Y-%m-%d")
    df = pd.read_sql(
        QUERY_HISTORY_TOP_RANKS,
        con=DBCON.engine,
        params={
            "store": store,
            "collection_id": collection_id,
            "category_id": category_id,
            "start_date": start_date,
            "mylimit": limit,
        },
    )
    return df


def get_store_collection_category_map() -> pd.DataFrame:
    """Get store collection and category map."""
    df = pd.read_sql(QUERY_STORE_COLLECTION_CATEGORY_MAP, con=DBCON.engine)
    return df


def get_category_top_apps_by_installs(category: str, limit: int = 10) -> pd.DataFrame:
    """Get category top apps sorted by installs."""
    logger.info(f"Query {category=} for top installs")
    df = pd.read_sql(
        QUERY_CATEGORY_TOP_APPS_BY_INSTALLS,
        DBCON.engine,
        params={"category": category, "mylimit": limit},
    )
    if not df.empty:
        df = clean_app_df(df)
    return df


def get_single_app(store_id: str) -> pd.DataFrame:
    """Get basic app details for a single store_id."""
    logger.info(f"Query for single app_id={store_id}")
    df = pd.read_sql(QUERY_SINGLE_APP, DBCON.engine, params={"store_id": store_id})
    if not df.empty:
        df = clean_app_df(df)
    return df


def get_app_package_details(store_id: str) -> pd.DataFrame:
    """Get basic app details for a single store_id."""
    logger.info(f"Query for single app_id={store_id}")
    df = pd.read_sql(
        QUERY_APP_PACKAGE_DETAILS,
        DBCON.engine,
        params={"store_id": store_id},
    )
    return df


def clean_app_df(df: pd.DataFrame) -> pd.DataFrame:
    """Apply generic cleaning for a DF with app data from store_apps table."""
    df["store"] = df["store"].replace({1: "Google Play", 2: "Apple App Store"})
    string_nums = ["installs", "review_count", "rating_count"]
    for col in string_nums:
        df[f"{col}_num"] = df[col]
        df[col] = df[col].apply(
            lambda x: "N/A" if (x is None or np.isnan(x)) else f"{x:,.0f}",
        )
    df["rating"] = df["rating"].apply(lambda x: round(x, 2) if x else 0)
    ios_link = "https://apps.apple.com/us/app/-/id"
    play_link = "https://play.google.com/store/apps/details?id="
    play_dev_link = "https://play.google.com/store/apps/dev?id="
    ios_dev_link = "https://apps.apple.com/us/developer/-/id"
    df["store_link"] = (
        np.where(df["store"].str.contains("Google"), play_link, ios_link)
        + df["store_id"]
    )
    if "developer_id" in df.columns:
        df["store_developer_link"] = np.where(
            df["store"].str.contains("Google"),
            play_dev_link,
            ios_dev_link,
        ) + df["developer_id"].astype(str)
    date_cols = ["created_at", "store_last_updated", "updated_at"]
    for x in date_cols:
        if x not in df.columns:
            continue
        df[x] = df[x].dt.strftime("%Y-%m-%d")
    return df


def get_app_history(store_app: int) -> pd.DataFrame:
    """Get scraping history for an app."""
    logger.info(f"Query for history single app_id={store_app}")
    df = pd.read_sql(QUERY_APP_HISTORY, DBCON.engine, params={"store_app": store_app})
    return df


def get_single_developer(developer_id: str) -> pd.DataFrame:
    """Get single developer details."""
    logger.info(f"Developers: {developer_id=}")
    df = pd.read_sql(
        QUERY_SINGLE_DEVELOPER,
        con=DBCON.engine,
        params={"developer_id": developer_id},
    )
    if not df.empty:
        df = clean_app_df(df)
    return df


def get_single_apps_adstxt(store_id: str) -> pd.DataFrame:
    """Get single developer's app ads txt entries."""
    logger.info(f"Query app's app-ads-txt: {store_id=}")
    df = pd.read_sql(
        QUERY_SINGLE_DEVELOPER_ADSTXT,
        con=DBCON.engine,
        params={"store_id": store_id},
    )
    return df


def get_apps_for_company(
    company_name: str,
    store_id: int,
    mapped_category: str,
    *,
    include_parents: bool = False,
) -> pd.DataFrame:
    """Get apps for for a network."""
    logger.info(f"Query: {company_name=} & {include_parents=}")

    if mapped_category == "games":
        mapped_category = "game%"

    if include_parents:
        df = pd.read_sql(
            QUERY_PARENT_COMPANY_APPS,
            con=DBCON.engine,
            params={
                "company_name": company_name,
                "store_id": store_id,
                "mapped_category": mapped_category,
                "mylimit": 20,
            },
        )
    else:
        df = pd.read_sql(
            QUERY_COMPANY_APPS,
            con=DBCON.engine,
            params={
                "company_name": company_name,
                "store_id": store_id,
                "mapped_category": mapped_category,
                "mylimit": 20,
            },
        )
    if not df.empty:
        df = clean_app_df(df)
    return df


def search_apps(search_input: str, limit: int = 100) -> pd.DataFrame:
    """Search apps by term in database."""
    logger.info(f"App search: {search_input=}")
    apps = pd.read_sql(
        QUERY_SEARCH_APPS,
        DBCON.engine,
        params={"searchinput": search_input, "mylimit": limit},
    )
    logger.info(f"App search devs: {search_input=}")
    devapps = pd.read_sql(
        QUERY_SEARCH_DEVS,
        DBCON.engine,
        params={"searchinput": search_input, "mylimit": limit},
    )
    logger.info(f"App search finished: {search_input=}")
    df = pd.concat([apps, devapps]).drop_duplicates()
    if not df.empty:
        df = clean_app_df(df)
    return df


def get_top_companies(
    categories: list[int],
    *,
    group_by_parent: bool = False,
) -> pd.DataFrame:
    """Get top networks, mmps or other companies.

    Data is pre-processed by materialized views.

    Args:
    ----
        categories (list[int]): list of 1=adnetworks, 2=MMP/Attribution, 3=Analytics.
        group_by_parent (bool): Group by a parent entity if such entity exists.

    """
    if group_by_parent:
        query = QUERY_TOP_PARENT_COMPANIES_MONTH
    else:
        query = QUERY_TOP_COMPANIES_MONTH

    df = pd.read_sql(query, DBCON.engine, params={"categories": tuple(categories)})

    return df


logger.info("set db engine")
DBCON = get_db_connection("madrone")
DBCON.set_engine()

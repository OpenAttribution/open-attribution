import datetime
import random
import time
import uuid

import pandas as pd
from clickhouse_connect import create_client

from config import get_logger
from tests._simulate_network_calls import click, impression, make_inapp_request

logger = get_logger(__name__)

"""
This will always generate a random campaign which gets
3 impressions
2 clicks
1 installs

with each 'user' rotates through the events in the order described. For example:
    1 impression -> 0 click -> 0 install
    1 impression -> 1 click -> 0 install
    1 impression -> 1 click -> 1 install
"""
NOT_ATTRIBUTABLE_SUFFIX = "_NOT_ATTRIBUTABLE"
APP = "com.example.one"

ADS = ["test1", "test2", "test3"]

NUM_INSTALLS = 1


ALL_TESTS = {
    "test_installs": {
        "1i_1c_1e": {
            "events": ["impression", "click", "app_open"],
            "is_attributable": True,
        },
        "1c_1e_1c_1e_1c_1e": {
            "events": ["click", "app_open", "click", "app_open", "click", "app_open"],
            "is_attributable": True,
        },
        "1i_1e_1i_1e_1i_1e": {
            "events": [
                "impression",
                "app_open",
                "impression",
                "app_open",
                "impression",
                "app_open",
            ],
            "is_attributable": True,
        },
        "1i_1e": {"events": ["impression", "app_open"], "is_attributable": True},
        "1c_1e": {"events": ["click", "app_open"], "is_attributable": True},
        "1i_2c_1e": {
            "events": ["impression", "click", "click", "app_open"],
            "is_attributable": True,
        },
        "2i_2c_1e_v2": {
            "events": ["impression", "impression", "click", "click", "app_open"],
            "is_attributable": True,
        },
        "2i_2c_1e": {
            "events": ["impression", "click", "impression", "click", "app_open"],
            "is_attributable": True,
        },
        "1i_1c_2e": {
            "events": ["impression", "click", "app_epen", "app_open"],
            "is_attributable": True,
        },
        "1i_1c_4e": {
            "events": [
                "impression",
                "click",
                "app_open",
                "app_open",
                "app_open",
                "app_open",
            ],
            "is_attributable": True,
        },
        "1i_1c_2e_1c_1e": {
            "events": [
                "impression",
                "click",
                "app_open",
                "app_open",
                "click",
                "app_open",
            ],
            "is_attributable": True,
        },
        "1i_1c_1e_1c_1e": {
            "events": [
                "impression",
                "click",
                "app_open",
                "click",
                "app_open",
            ],
            "is_attributable": True,
        },
        "1i_1c_1e_1c_1e_1c_1e": {
            "events": [
                "impression",
                "click",
                "app_open",
                "app_open",
                "click",
                "app_open",
                "click",
                "app_open",
            ],
            "is_attributable": True,
        },
        "1i_1c_1e_1e_1c_1e_1c_1c_1i": {
            "events": [
                "impression",
                "click",
                "app_open",
                "app_open",
                "click",
                "app_open",
                "click",
                "click",
                "impression",
            ],
            "is_attributable": True,
        },
        "1i_1c_4e_1c_1e": {
            "events": [
                "impression",
                "click",
                "app_open",
                "app_open",
                "app_open",
                "app_open",
                "click",
                "app_open",
            ],
            "is_attributable": True,
        },
        "1i_1c_4e_1c_3e": {
            "events": [
                "impression",
                "click",
                "app_open",
                "app_open",
                "app_open",
                "app_open",
                "click",
                "app_open",
                "app_open",
                "app_open",
            ],
            "is_attributable": True,
        },
        "1i_1c_4e_1i_3e": {
            "events": [
                "impression",
                "click",
                "app_open",
                "app_open",
                "app_open",
                "app_open",
                "impression",
                "app_open",
                "app_open",
                "app_open",
            ],
            "is_attributable": True,
        },
        "1i_1c_4e_1i_3e_1i_2e": {
            "events": [
                "impression",
                "click",
                "app_open",
                "app_open",
                "app_open",
                "app_open",
                "impression",
                "app_open",
                "app_open",
                "app_open",
                "impression",
                "app_open",
                "app_open",
            ],
            "is_attributable": True,
        },
        "1i_1c_2e_1i_1e": {
            "events": [
                "impression",
                "click",
                "app_open",
                "app_open",
                "impression",
                "app_open",
            ],
            "is_attributable": True,
        },
        "1i_1c_2e_1i_1c_2e": {
            "events": [
                "impression",
                "click",
                "app_open",
                "app_open",
                "impression",
                "click",
                "app_open",
                "app_open",
            ],
            "is_attributable": True,
        },
        "1i_1c_1e_1t": {
            "events": ["impression", "click", "app_open", "tutorial"],
            "is_attributable": True,
        },
        "1i_1c_1e_2t": {
            "events": ["impression", "click", "app_open", "tutorial", "level1"],
            "is_attributable": True,
        },
        "1i_1c_0e": {"events": ["impression", "click"], "is_attributable": False},
        "1i_0e": {
            "events": [
                "impression",
            ],
            "is_attributable": False,
        },
        "1c_0e": {"events": ["click"], "is_attributable": False},
        "2i_2c_0e": {
            "events": ["impression", "click", "impression", "click"],
            "is_attributable": False,
        },
    },
}


def get_expected_test_df(time_part: str) -> pd.DataFrame:
    test_df = pd.DataFrame(ALL_TESTS)
    test_df = test_df.reset_index().rename(columns={"index": "campaign_name"})
    test_df = (
        pd.concat(
            [
                test_df.drop(columns="test_installs"),
                pd.json_normalize(test_df["test_installs"]),
            ],
            axis=1,
        )
        .explode("events")
        .groupby(["campaign_name", "events", "is_attributable"])
        .size()
        .reset_index()
        .rename(columns={0: "count"})
    )
    test_df["num_users"] = NUM_INSTALLS
    test_df["total_count"] = NUM_INSTALLS * test_df["count"]
    test_df["installs"] = test_df["num_users"] * test_df["is_attributable"]
    test_df = (
        pd.pivot(
            test_df,
            index=["campaign_name", "is_attributable", "installs"],
            columns="events",
            values="total_count",
        )
        .fillna(0)
        .reset_index()
        .rename(
            columns={
                "installs": "expected_installs",
                "impression": "expected_impressions",
                "click": "expected_clicks",
            },
        )
    )
    test_df["campaign_name"] = test_df["campaign_name"] + f"_{time_part}"
    test_df = test_df[
        [
            "campaign_name",
            "expected_impressions",
            "expected_clicks",
            "expected_installs",
        ]
    ]
    return test_df


client = create_client(host="localhost")


def query_campaign(table: str, campaign: str) -> pd.DataFrame:
    bad_name = campaign + NOT_ATTRIBUTABLE_SUFFIX
    # Define the query template
    query_template = """
    SELECT
        *
    FROM
        %(table)s
    WHERE
        campaign_name = %(campaign_name)s OR campaign_name = %(bad_name)s
    """
    # Execute the query and fetch the data as pandas df
    df = client.query_df(
        query_template,
        parameters={"campaign_name": campaign, "table": table, "bad_name": bad_name},
    )
    if not df.empty:
        # NOTE: Since some campaigns have suffixes to warn if they show up in data, ignore those names here
        df["original_campaign_name"] = df["campaign_name"]
    df["campaign_name"] = campaign
    return df


def get_db_data_for_single_campaign(campaign: str) -> pd.DataFrame:
    tables = ["impressions", "clicks"]
    dfs = []
    for table in tables:
        df = query_campaign(table=table, campaign=campaign)
        df["type"] = table
        dfs.append(df)
    df = pd.concat(dfs)
    if df.empty:
        logger.warning(f"Testing did not find any data in db for {campaign=}")
    else:
        df = (
            df.groupby(["campaign_name", "type"])
            .size()
            .reset_index()
            .rename(columns={0: "db_raw_count"})
        )
        df = (
            pd.pivot(df, index="campaign_name", columns="type", values="db_raw_count")
            .add_prefix("raw_")
            .reset_index()
        )
    odf = query_campaign(table="daily_overview", campaign=campaign)
    if odf.empty:
        logger.warning(f"Testing did not find any data in db for {campaign=}")
    else:
        odf = (
            odf.groupby(["campaign_name"])[["impressions", "clicks", "installs"]]
            .sum()
            .add_prefix("overview_")
            .reset_index()
        )
    try:
        campaign_df = pd.merge(df, odf, how="outer", on="campaign_name", validate="1:1")
    except Exception:
        logger.exception(f"Testing did not find any data in db for {campaign=}")
    return campaign_df


def get_db_dfs(time_part: str) -> pd.DataFrame:
    db_dfs = []
    for _campaign in ALL_TESTS["test_installs"].keys():
        campaign = _campaign + "_" + time_part
        campaign_df = get_db_data_for_single_campaign(campaign)
        db_dfs.append(campaign_df)
    db_df = pd.concat(db_dfs)
    return db_df


def check_install_results(time_part: str) -> None:
    logger.info("Begin checking results")
    test_df = get_expected_test_df(time_part)
    db_df = get_db_dfs(time_part)

    df = pd.merge(
        test_df,
        db_df,
        how="outer",
        on="campaign_name",
        validate="1:1",
    ).fillna(0)
    df["raw_impressions_ok"] = df["expected_impressions"] == df["raw_impressions"]
    df["raw_clicks_ok"] = df["expected_clicks"] == df["raw_clicks"]
    df["overview_impressions_ok"] = (
        df["expected_impressions"] == df["overview_impressions"]
    )
    df["overview_clicks_ok"] = df["expected_clicks"] == df["overview_clicks"]
    df["overview_installs_ok"] = df["expected_installs"] == df["overview_installs"]
    row_checks = [
        "raw_impressions_ok",
        "raw_clicks_ok",
        "overview_impressions_ok",
        "overview_clicks_ok",
        "overview_installs_ok",
    ]
    df["all_ok"] = df[row_checks].all(axis=1)
    for _idx, row in df.iterrows():
        if row.all_ok:
            logger.info(f"{row.campaign_name=} is OK!")
        else:
            logger.error(f"{row.campaign_name=} is NOK!")
            logger.info(f"{row.campaign_name=} check: {row}")


def main() -> None:
    test_time = datetime.datetime.now(tz=datetime.UTC).strftime("%Y%m%d%H%M_%S")
    for network, tests in ALL_TESTS.items():
        for _campaign, test in tests.items():
            if isinstance(test["events"], list):
                my_events: list[str] = test["events"]
            else:
                logger.warning(
                    f"campaign test: {_campaign} is incorrectly formatted, events must be a list.",
                )
                continue
            _total_impressions = 0
            _total_clicks = 0
            _total_events = 0
            campaign = _campaign + "_" + test_time
            for _ in range(NUM_INSTALLS):
                ifa = str(uuid.uuid4())  # User start
                ad = random.choice(ADS)
                for idx, item in enumerate(my_events):
                    if item in ["impression", "click"]:
                        if "app_open" in test["events"][:idx]:
                            my_campaign = campaign + NOT_ATTRIBUTABLE_SUFFIX
                        else:
                            my_campaign = campaign
                        if item == "impression":
                            impression(
                                myapp=APP,
                                mycampaign=my_campaign,
                                mynetwork=network,
                                myifa=ifa,
                                myad=ad,
                            )
                            _total_impressions += 1
                        elif item == "click":
                            click(
                                myapp=APP,
                                mycampaign=my_campaign,
                                mynetwork=network,
                                myifa=ifa,
                                myad=ad,
                            )
                            _total_clicks += 1
                    else:
                        time.sleep(0.5)  # Simulate delay
                        make_inapp_request(
                            event_id=item,
                            myapp=APP,
                            myifa=ifa,
                        )
                        _total_events += 1
            logger.info(
                f"{campaign} index:{_} impressions:{_total_impressions} clicks: {_total_clicks} events:{_total_events} ",
            )
    logger.info("Pause before checking")
    time.sleep(10)
    check_install_results(time_part=test_time)

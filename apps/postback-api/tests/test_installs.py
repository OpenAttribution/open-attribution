import datetime
import secrets
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

NUM_INSTALLS = 3


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
        "1i_1c_1i_1c_1e": {
            "events": ["impression", "click", "impression", "click", "app_open"],
            "is_attributable": True,
        },
        "2i_2c_1e": {
            "events": ["impression", "impression", "click", "click", "app_open"],
            "is_attributable": True,
        },
        "1i_1c_2e": {
            "events": ["impression", "click", "app_open", "app_open"],
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
        "1i_1c_2e_1c_1e_1c_1e": {
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
        "1i_1c_2e_1c_1e_2c_1i": {
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
        "1i_1c_1i_1c_0e": {
            "events": ["impression", "click", "impression", "click"],
            "is_attributable": False,
        },
    },
}


def get_expected_test_df(run_tests: dict, time_part: str) -> pd.DataFrame:
    test_df = pd.DataFrame.from_dict(run_tests, orient="index")
    test_df = test_df.reset_index().rename(columns={"index": "campaign_name"})
    test_df = (
        test_df.explode("events")
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
    expected_cols = ["expected_installs", "expected_clicks", "exptected_impressions"]
    for col in expected_cols:
        if col not in test_df.columns:
            test_df[col] = 0
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


def query_campaign(table: str, campaign: str) -> pd.DataFrame:
    """Query data from clickhouse."""
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
    client = create_client(host="clickhouse")
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
    tables = ["impressions", "clicks", "attributed_installs"]
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


def get_db_dfs(run_tests: dict, time_part: str) -> pd.DataFrame:
    db_dfs = []
    for _campaign in run_tests:
        campaign = _campaign + "_" + time_part
        campaign_df = get_db_data_for_single_campaign(campaign)
        db_dfs.append(campaign_df)
    db_df = pd.concat(db_dfs)
    expected_cols = [
        "raw_attributed_installs",
        "raw_clicks",
        "raw_impressions",
        "overview_installs",
        "overview_clicks",
        "overview_impressions",
    ]
    for col in expected_cols:
        if col not in db_df.columns:
            db_df[col] = 0
    return db_df


def check_install_results(run_tests: dict, time_part: str) -> None:
    logger.info("Begin checking results")
    test_df = get_expected_test_df(run_tests, time_part)
    db_df = get_db_dfs(run_tests, time_part)
    df = pd.merge(
        test_df,
        db_df,
        how="outer",
        on="campaign_name",
        validate="1:1",
    ).fillna(0)
    df["raw_impressions_ok"] = df["expected_impressions"] == df["raw_impressions"]
    df["raw_clicks_ok"] = df["expected_clicks"] == df["raw_clicks"]
    df["raw_installs_ok"] = df["expected_installs"] == df["raw_attributed_installs"]
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


def main(endpoint: str, test_names: list[str] | None = None) -> None:
    """Run tests and check results."""
    time_part = datetime.datetime.now(tz=datetime.UTC).strftime("%Y%m%d%H%M_%S")
    for network, tests in ALL_TESTS.items():
        if test_names:
            run_tests = {key: tests[key] for key in test_names if key in tests}
            if len(run_tests) == 0:
                example_test_names = " or ".join(list(tests.keys())[0:2])
                logger.error(
                    f"No test names matched, try names like {example_test_names} from test_installs.py",
                )
                return
            logger.info(f"tests filtered to {len(run_tests)} out of {len(tests)}.")
        else:
            run_tests = tests
        for _campaign, test in run_tests.items():
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
            campaign = _campaign + "_" + time_part
            for _ in range(NUM_INSTALLS):
                ifa = str(uuid.uuid4())  # User start
                oa_uid = str(uuid.uuid4())  # User start
                ad = secrets.choice(ADS)
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
                                endpoint=endpoint,
                            )
                            _total_impressions += 1
                        elif item == "click":
                            click(
                                myapp=APP,
                                mycampaign=my_campaign,
                                mynetwork=network,
                                myifa=ifa,
                                myad=ad,
                                endpoint=endpoint,
                            )
                            _total_clicks += 1
                    else:
                        time.sleep(0.5)  # Simulate delay
                        make_inapp_request(
                            event_id=item,
                            myapp=APP,
                            myifa=ifa,
                            my_oa_uid=oa_uid,
                            endpoint=endpoint,
                        )
                        _total_events += 1
            logger.info(
                f"{campaign} index:{_} impressions:{_total_impressions} clicks: {_total_clicks} events:{_total_events} ",
            )
    logger.info("Pause before checking")
    time.sleep(20)
    check_install_results(run_tests=run_tests, time_part=time_part)

import datetime
import random
import time
import uuid

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

APP = "com.example.one"

ADS = ["test1", "test2", "test3"]


NUM_INSTALLS = 5

ALL_TESTS = {
    "test_installs_5": {
        "1i_1c_1e": ["impression", "click", "app_open"],
        "1i_0c_1e": ["impression", "app_open"],
        "0i_1c_1e": ["click", "app_open"],
        "1i_2c_1e": ["impression", "click", "click", "app_open"],
        "2i_2c_1e_v2": ["impression", "impression", "click", "click", "app_open"],
        "2i_2c_1e": ["impression", "click", "impression", "click", "app_open"],
        "1i_1c_2e": ["impression", "click", "event", "app_open"],
        "1i_1c_2e_1c_1e": [
            "impression",
            "click",
            "app_open",
            "app_open",
            "click",
            "app_open",
        ],
        "1i_1c_2e_1i_1e": [
            "impression",
            "click",
            "app_open",
            "app_open",
            "impression",
            "app_open",
        ],
        "1i_1c_1e_1t": ["impression", "click", "app_open", "tutorial"],
        "1i_1c_1e_2t": ["impression", "click", "app_open", "tutorial", "level1"],
    },
    "test_installs_0": {
        "1i_1c_0e": ["impression", "click"],
        "1i_0c_0e": [
            "impression",
        ],
        "0i_1c_0e": ["click"],
        "2i_2c_0e": ["impression", "click", "impression", "click"],
    },
}


def main() -> None:
    test_time = datetime.datetime.now(tz=datetime.UTC).strftime("%Y%m%d%H%M")
    for network, tests in ALL_TESTS.items():
        for _campaign, test in tests.items():
            _total_impressions = 0
            _total_clicks = 0
            _total_installs = 0
            campaign = _campaign + "_" + test_time
            for _ in range(NUM_INSTALLS):
                ifa = str(uuid.uuid4())  # User start
                ad = random.choice(ADS)
                for idx, item in enumerate(test):
                    if item in ["impression", "click"]:
                        if "app_open" in test[:idx]:
                            my_campaign = campaign + "_BAD_RESULT"
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
                        elif item == "click":
                            click(
                                myapp=APP,
                                mycampaign=my_campaign,
                                mynetwork=network,
                                myifa=ifa,
                                myad=ad,
                            )
                    else:
                        make_inapp_request(
                            event_id=item,
                            myapp=APP,
                            myifa=ifa,
                        )
                    time.sleep(random.uniform(0.1, 0.5))  # Simulate delay
            logger.info(
                f"{campaign} index:{_} impressions:{_total_impressions} clicks: {_total_clicks} installs:{_total_installs} "
            )

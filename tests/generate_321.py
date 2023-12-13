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

with each 'user' rotates through:
    1 impression -> 1 click -> 1 install
    1 impression -> 1 click -> 0 install
    1 impression -> 0 click -> 0 install
"""

NETWORKS = [
    "test_321",
]
APPS = ["com.example.one", "123456789"]
APPS = ["com.example.one"]

ADS = ["test2", "test1", "test3"]


NUM_INSTALLS = 20


def main() -> None:
    _total_impressions = 0
    _total_clicks = 0
    _total_installs = 0
    for network in NETWORKS:
        for app in APPS:
            campaign = "test_" + datetime.datetime.now(tz=datetime.UTC).strftime(
                "%Y%m%d%H%M"
            )
            for _ in range(NUM_INSTALLS):
                num_impressions = 0
                num_installs = 0
                num_clicks = 0
                while num_impressions < 3:
                    num_impressions += 1
                    _total_impressions += 1
                    ifa = str(uuid.uuid4())  # User start
                    ad = random.choice(ADS)
                    impression(
                        myapp=app,
                        mycampaign=campaign,
                        mynetwork=network,
                        myifa=ifa,
                        myad=ad,
                    )
                    if num_clicks < 2:
                        num_clicks += 1
                        _total_clicks += 1
                        time.sleep(random.uniform(0.1, 0.3))  # Simulate delay
                        click(
                            myapp=app,
                            mycampaign=campaign,
                            mynetwork=network,
                            myifa=ifa,
                            myad=ad,
                        )
                    if num_installs == 0:
                        num_installs += 1
                        _total_installs += 1
                        time.sleep(random.uniform(0.1, 1.0))  # Simulate delay
                        make_inapp_request(
                            mytype="events",
                            event_id="app_open",
                            myapp=app,
                            myifa=ifa,
                        )
                logger.info(
                    f"index:{_} impressions:{_total_impressions} clicks: {_total_clicks} installs:{_total_installs} "
                )

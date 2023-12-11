import datetime
import random
import time
import uuid

from config import get_logger
from tests._simulate_network_calls import impression_or_click, make_inapp_request

logger = get_logger(__name__)

"""
This will always generate a random campaign which gets
300 impressions
200 clicks
100 installs

with each 'user' one of:
    1 impression > 1 click > 1 install
    1 impression > 1 click > 0 install
    1 impression > 0 click > 0 install
"""

NETWORKS = [
    "test_321",
]
APPS = ["com.example.one", "123456789"]

ADS = ["test2", "test1", "test3"]


NUM_INSTALLS = 20


def main() -> None:
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
                    ifa = str(uuid.uuid4())
                    ad = random.choice(ADS)
                    impression_or_click(
                        mytype="impressions",
                        myapp=app,
                        mycampaign=campaign,
                        mynetwork=network,
                        myifa=ifa,
                        myad=ad,
                    )
                    while num_clicks < 2:
                        num_clicks += 1
                        time.sleep(random.uniform(0.1, 0.3))  # Simulate delay
                        impression_or_click(
                            mytype="clicks",
                            myapp=app,
                            mycampaign=campaign,
                            mynetwork=network,
                            myifa=ifa,
                            myad=ad,
                        )
                        while num_installs < 1:
                            num_installs += 1
                            time.sleep(random.uniform(0.1, 1.0))  # Simulate delay
                            make_inapp_request(
                                mytype="events",
                                event_id="app_open",
                                myapp=app,
                                myifa=ifa,
                            )

import datetime
import random
import time
import uuid

import requests

from config import get_logger
from config.dimensions import (
    APP_EVENT_TIME,
    LINK_AD,
    LINK_APP_EVENT_ID,
    LINK_CAMPAIGN,
    LINK_IFA,
    LINK_NETWORK,
)

logger = get_logger(__name__)


ENDPOINT = "http://localhost:8000/collect"


NETWORKS = ["google", "ironsource", "facebook"]
APPS = ["com.example.one", "com.game.eg.gg", "id123456789", "123456789"]

CAMPAIGNS = ["CampaignA", "CampaignB"]

ADS = ["Hi!", "NewVideo123"]


def make_request(
    mytype: str, myapp: str, mycampaign: str, myifa: str, mynetwork: str, myad: str
) -> None:
    params = {
        LINK_CAMPAIGN: mycampaign,
        LINK_IFA: myifa,
        LINK_NETWORK: mynetwork,
        LINK_AD: myad,
    }
    url = ENDPOINT + f"/{mytype}/{myapp}"
    response = requests.get(url, params=params)
    logger.info(f"GET {response.status_code} {url=} ")
    return


def make_inapp_request(mytype: str, myapp: str, event_id: str, myifa: str) -> None:
    params = {
        LINK_APP_EVENT_ID: event_id,
        LINK_IFA: myifa,
        APP_EVENT_TIME: datetime.datetime.now(datetime.timezone.utc),
    }
    url = ENDPOINT + f"/{mytype}/{myapp}"
    response = requests.get(url, params=params)
    logger.info(f"GET {response.status_code} {url=} ")
    return


def main() -> None:
    while True:
        for network in NETWORKS:
            for app in APPS:
                if random.random() < 0.3:
                    # Simulate organic install and return
                    ifa = str(uuid.uuid4())
                    make_inapp_request(
                        mytype="events",
                        event_id="app_open",
                        myapp=app,
                        myifa=ifa,
                    )
                    continue
                for campaign in CAMPAIGNS:
                    ifa = str(uuid.uuid4())
                    for ad in ADS:
                        make_request(
                            mytype="impressions",
                            myapp=app,
                            mycampaign=campaign,
                            mynetwork=network,
                            myifa=ifa,
                            myad=ad,
                        )
                        # Decide if a click should be generated
                        if random.random() < 0.5:  # % chance for a click
                            time.sleep(random.uniform(0.1, 1.0))  # Simulate delay
                            make_request(
                                mytype="clicks",
                                myapp=app,
                                mycampaign=campaign,
                                mynetwork=network,
                                myifa=ifa,
                                myad=ad,
                            )
                            if random.random() < 0.5:
                                time.sleep(random.uniform(0.1, 1.0))  # Simulate delay
                                make_inapp_request(
                                    mytype="events",
                                    event_id="app_open",
                                    myapp=app,
                                    myifa=ifa,
                                )

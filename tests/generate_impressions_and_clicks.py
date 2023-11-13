import random
import time
import uuid

import requests

from config import get_logger
from config.dimensions import (
    LINK_AD,
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
    requests.get(url, params=params)
    logger.info(f"{url=} with {params=}")
    return


def main() -> None:
    for network in NETWORKS:
        for app in APPS:
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
                    if random.random() < 0.03:  # 3% chance for a click
                        time.sleep(random.uniform(0.5, 2.0))  # Simulate delay
                        make_request(
                            mytype="clicks",
                            myapp=app,
                            mycampaign=campaign,
                            mynetwork=network,
                            myifa=ifa,
                            myad=ad,
                        )
                    time.sleep(random.uniform(0.5, 2.0))  # Simulate delay

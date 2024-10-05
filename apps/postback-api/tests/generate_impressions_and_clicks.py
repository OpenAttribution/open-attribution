"""Generate impressions and clicks for testing."""

import random
import time
import uuid

from config import get_logger

from tests._simulate_network_calls import impression_or_click, make_inapp_request

logger = get_logger(__name__)

NETWORKS = ["google", "ironsource", "facebook"]
APPS = ["com.example.one", "com.game.eg.gg", "id123456789", "123456789"]

CAMPAIGNS = ["CampaignA", "CampaignB"]

ADS = ["Hi!", "NewVideo123"]

INSTALL_RATE = 0.3
CLICK_THROUGH_RATE = 0.5
D1_APP_OPEN_RATE = 0.4


def main(endpoint: str) -> None:
    """Start here."""
    logger.info("Start continuous generate")
    while True:
        for network in NETWORKS:
            for app in APPS:
                if random.random() < INSTALL_RATE:  # noqa: S311
                    # Simulate organic install and return
                    ifa = str(uuid.uuid4())
                    make_inapp_request(
                        event_id="app_open",
                        myapp=app,
                        myifa=ifa,
                        endpoint=endpoint,
                    )
                    continue
                for campaign in CAMPAIGNS:
                    ifa = str(uuid.uuid4())
                    for ad in ADS:
                        impression_or_click(
                            mytype="impressions",
                            myapp=app,
                            mycampaign=campaign,
                            mynetwork=network,
                            myifa=ifa,
                            myad=ad,
                            endpoint=endpoint,
                        )
                        # Decide if a click should be generated
                        if random.random() < CLICK_THROUGH_RATE:  # noqa: S311
                            time.sleep(random.uniform(0.1, 1.0))  # noqa: S311
                            impression_or_click(
                                mytype="clicks",
                                myapp=app,
                                mycampaign=campaign,
                                mynetwork=network,
                                myifa=ifa,
                                myad=ad,
                                endpoint=endpoint,
                            )
                            if random.random() < D1_APP_OPEN_RATE:  # noqa: S311
                                time.sleep(random.uniform(0.1, 1.0))  # noqa: S311
                                make_inapp_request(
                                    event_id="app_open",
                                    myapp=app,
                                    myifa=ifa,
                                    endpoint=endpoint,
                                )

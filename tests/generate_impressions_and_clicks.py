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
                        impression_or_click(
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
                            impression_or_click(
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

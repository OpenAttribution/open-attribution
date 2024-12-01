"""Generate impressions and clicks for testing."""

# ruff: noqa: S311

import random
import time
import uuid

from config import get_logger

from tests._simulate_network_calls import impression_or_click, make_inapp_request

logger = get_logger(__name__)

NETWORKS = ["google", "ironsource", "meta"]
APPS = ["com.example.one", "com.game.eg.gg", "id123456789", "123456789"]

CAMPAIGNS = ["CampaignA", "CampaignB"]

ADS = ["Hi!", "NewVideo123"]

INSTALL_RATE = 0.3
CLICK_THROUGH_RATE = 0.5
D1_APP_OPEN_RATE = 0.4

def generate_random_ip() -> str:
    """
    Generate a random ip address.

    Returns:
        str: A random ip address.

    """
    # Avoid reserved ranges by using common public IP ranges
    first_octet = random.choice([203, 8, 34, 50, 66, 98, 172, 177, 178])
    return f"{first_octet}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"



def main(endpoint: str) -> None:
    """Start here."""
    logger.info("Start continuous generate")
    while True:
        for network in NETWORKS:
            for app in APPS:
                if random.random() < INSTALL_RATE:
                    # Simulate organic install and return
                    ifa = str(uuid.uuid4())
                    oa_uid = str(uuid.uuid4())
                    random_ip = generate_random_ip()
                    headers = {
                        "X-Forwarded-For": random_ip,
        "X-Real-IP": random_ip,
    }
                    make_inapp_request(
                        event_id="app_open",
                        myapp=app,
                        myifa=ifa,
                        my_oa_uid=oa_uid,
                        headers=headers,
                        endpoint=endpoint,
                    )
                    continue
                for campaign in CAMPAIGNS:
                    ifa = str(uuid.uuid4())
                    random_ip = generate_random_ip()
                    headers = {
                        "X-Forwarded-For": random_ip,
        "X-Real-IP": random_ip,
    }
                    for ad in ADS:
                        impression_or_click(
                            mytype="impressions",
                            myapp=app,
                            mycampaign=campaign,
                            mynetwork=network,
                            myifa=ifa,
                            myad=ad,
                            headers=headers,
                            endpoint=endpoint,
                        )
                        # Decide if a click should be generated
                        if random.random() < CLICK_THROUGH_RATE:
                            oa_uid = str(uuid.uuid4())
                            time.sleep(random.uniform(0.1, 1.0))
                            impression_or_click(
                                mytype="clicks",
                                myapp=app,
                                mycampaign=campaign,
                                mynetwork=network,
                                myifa=ifa,
                                myad=ad,
                                endpoint=endpoint,
                            )
                            if random.random() < D1_APP_OPEN_RATE:
                                time.sleep(random.uniform(0.1, 1.0))
                                make_inapp_request(
                                    event_id="app_open",
                                    myapp=app,
                                    myifa=ifa,
                                    my_oa_uid=oa_uid,
                                    endpoint=endpoint,
                                )

import datetime

import requests

from config import get_logger
from config.dimensions import (
    APP_EVENT_TIME,
    LINK_AD,
    LINK_APP_EVENT_ID,
    LINK_CAMPAIGN,
    LINK_EVENT_TIME,
    LINK_IFA,
    LINK_NETWORK,
)

logger = get_logger(__name__)

ENDPOINT = "http://localhost:8000/collect"


def impression_or_click(
    mytype: str, myapp: str, mycampaign: str, myifa: str, mynetwork: str, myad: str
) -> None:
    tmstmp: str = str(
        round(datetime.datetime.now(datetime.timezone.utc).timestamp() * 1000)
    )
    params = {
        LINK_CAMPAIGN: mycampaign,
        LINK_IFA: myifa,
        LINK_NETWORK: mynetwork,
        LINK_AD: myad,
        LINK_EVENT_TIME: tmstmp,
    }
    url = ENDPOINT + f"/{mytype}/{myapp}"
    response = requests.get(url, params=params)
    logger.info(f"GET {response.status_code} {url=} ")
    return


def make_inapp_request(mytype: str, myapp: str, event_id: str, myifa: str) -> None:
    tmstmp: str = str(
        round(datetime.datetime.now(datetime.timezone.utc).timestamp() * 1000)
    )
    params = {
        LINK_APP_EVENT_ID: event_id,
        LINK_IFA: myifa,
        APP_EVENT_TIME: tmstmp,
    }
    url = ENDPOINT + f"/{mytype}/{myapp}"
    response = requests.get(url, params=params)
    logger.info(f"GET {response.status_code} {url=} ")
    return

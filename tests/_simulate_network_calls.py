import datetime
import uuid

import requests

from config import get_logger
from config.dimensions import (
    APP_EVENT_TIME,
    APP_EVENT_UID,
    LINK_AD,
    LINK_APP_EVENT_ID,
    LINK_CAMPAIGN,
    LINK_EVENT_TIME,
    LINK_IFA,
    LINK_NETWORK,
    LINK_UID,
)

logger = get_logger(__name__)

ENDPOINT = "http://localhost:8000/collect"


def impression(
    myapp: str, mycampaign: str, myifa: str, mynetwork: str, myad: str
) -> None:
    impression_or_click(
        mytype="impressions",
        myapp=myapp,
        mycampaign=mycampaign,
        mynetwork=mynetwork,
        myifa=myifa,
        myad=myad,
    )


def click(myapp: str, mycampaign: str, myifa: str, mynetwork: str, myad: str) -> None:
    impression_or_click(
        mytype="clicks",
        myapp=myapp,
        mycampaign=mycampaign,
        mynetwork=mynetwork,
        myifa=myifa,
        myad=myad,
    )


def impression_or_click(
    mytype: str, myapp: str, mycampaign: str, myifa: str, mynetwork: str, myad: str
) -> None:
    tmstmp: str = str(
        round(datetime.datetime.now(datetime.timezone.utc).timestamp() * 1000)
    )
    id = str(uuid.uuid4())
    params = {
        LINK_CAMPAIGN: mycampaign,
        LINK_IFA: myifa,
        LINK_NETWORK: mynetwork,
        LINK_AD: myad,
        LINK_EVENT_TIME: tmstmp,
        LINK_UID: id,
    }
    url = ENDPOINT + f"/{mytype}/{myapp}"
    response = requests.get(url, params=params)
    logger.info(f"GET {response.status_code} {url=} {id=} ")
    return


def make_inapp_request(mytype: str, myapp: str, event_id: str, myifa: str) -> None:
    tmstmp: str = str(
        round(datetime.datetime.now(datetime.timezone.utc).timestamp() * 1000)
    )
    id = str(uuid.uuid4())
    params = {
        LINK_APP_EVENT_ID: event_id,
        LINK_IFA: myifa,
        APP_EVENT_TIME: tmstmp,
        APP_EVENT_UID: id,
    }
    url = ENDPOINT + f"/{mytype}/{myapp}"
    response = requests.get(url, params=params)
    logger.info(f"GET {response.status_code} {url=} ")
    return

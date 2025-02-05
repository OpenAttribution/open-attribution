import datetime
import uuid

import requests
from config import get_logger
from config.dimensions import (
    APP_EVENT_TIME,
    APP_EVENT_UID,
    APP_OA_USER_ID,
    LINK_AD,
    LINK_APP_EVENT_ID,
    LINK_CAMPAIGN,
    LINK_EVENT_TIME,
    LINK_IFA,
    LINK_NETWORK,
    LINK_UID,
)

logger = get_logger(__name__)


def impression(
    myapp: str,
    mycampaign: str,
    myifa: str,
    mynetwork: str,
    myad: str,
    endpoint: str,
    headers: dict,
) -> None:
    impression_or_click(
        mytype="impressions",
        myapp=myapp,
        mycampaign=mycampaign,
        mynetwork=mynetwork,
        myifa=myifa,
        myad=myad,
        headers=headers,
        endpoint=endpoint,
    )


def click(
    myapp: str,
    mycampaign: str,
    myifa: str,
    mynetwork: str,
    myad: str,
    endpoint: str,
    headers: dict,
) -> None:
    impression_or_click(
        mytype="clicks",
        myapp=myapp,
        mycampaign=mycampaign,
        mynetwork=mynetwork,
        myifa=myifa,
        myad=myad,
        headers=headers,
        endpoint=endpoint,
    )


def impression_or_click(
    mytype: str,
    myapp: str,
    mycampaign: str,
    myifa: str,
    mynetwork: str,
    myad: str,
    headers: dict,
    endpoint: str,
) -> None:
    tmstmp: str = str(
        round(datetime.datetime.now(datetime.UTC).timestamp() * 1000),
    )
    uid = str(uuid.uuid4())
    params = {
        LINK_CAMPAIGN: mycampaign,
        LINK_IFA: myifa,
        LINK_NETWORK: mynetwork,
        LINK_AD: myad,
        LINK_EVENT_TIME: tmstmp,
        LINK_UID: uid,
    }
    url = endpoint + f"/collect/{mytype}/{myapp}"
    response = requests.get(url, params=params, headers=headers, timeout=10)
    logger.info(f"GET {response.status_code} {mytype.upper()} {url=} {uid=} ")


def make_inapp_request(
    myapp: str,
    event_id: str,
    myifa: str,
    my_oa_uid: str,
    headers: dict,
    endpoint: str,
    offset_days: int = 0,
) -> None:
    tmstmp: str = str(
        round(
            (
                datetime.datetime.now(datetime.UTC)
                + datetime.timedelta(days=offset_days)
            ).timestamp()
            * 1000,
        ),
    )
    uid = str(uuid.uuid4())
    params = {
        LINK_APP_EVENT_ID: event_id,
        LINK_IFA: myifa,
        APP_EVENT_TIME: tmstmp,
        APP_EVENT_UID: uid,
        APP_OA_USER_ID: my_oa_uid,
    }
    url = endpoint + f"/collect/events/{myapp}"
    response = requests.get(url, params=params, headers=headers, timeout=10)
    logger.info(f"GET {response.status_code} EVENTS {url=} {params=} ")

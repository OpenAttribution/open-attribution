"""
API endpoints for share links.

Any URL to /s/ will look up the data in the database
and then redirect to the landing page with the web SDK
that checks if the user has already installed the app.


Endpoints for Share Links
=========
/s/

"""

import json
from typing import Self

import requests
from config import CLICK_PRODUCER, get_logger
from config.dimensions import (
    DB_AD_ID,
    DB_AD_NAME,
    DB_C,
    DB_C_ID,
    DB_CITY_NAME,
    DB_CLIENT_IP,
    DB_COUNTRY_ISO,
    DB_IFA,
    DB_LINK_UID,
    DB_NETWORK,
    DB_RECEIVED_AT,
    DB_STATE_ISO,
    DB_STORE_ID,
)
from confluent_kafka import KafkaException
from dbcon.queries import APP_LINKS
from detect.geo import get_geo
from litestar import BackgroundTask, Controller, RedirectResponse, Request, get
from litestar.exceptions import HTTPException

from api_app.tools import EMPTY_IFA, generate_link_uid, get_client_ip, now

logger = get_logger(__name__)


def get_admin_link_data(share_slug: str) -> dict:
    """Get the link data from the admin API."""
    response = requests.get(f"http://localhost:8001/links/{share_slug}", timeout=10)
    response.raise_for_status()
    return response.json()


def process_share_link(share_slug: str, client_host: str, link_uid: str) -> None:
    """Process the share link in background."""
    try:
        link_data = get_admin_link_data(share_slug)
    except requests.exceptions.RequestException as ex:
        logger.exception("Failed to get link data from admin API.")
        raise HTTPException(status_code=500, detail=ex.args[0].str()) from ex

    event_time = now()
    ifa = EMPTY_IFA
    source = link_data.get("network")
    app = link_data.get("store_id")
    c = link_data.get("campaign")
    c_id = link_data.get("campaign_id")
    ad = link_data.get("ad")
    ad_id = link_data.get("ad_id")

    geo_data = get_geo(client_host)
    country_iso = geo_data.get("country_iso")
    state_iso = geo_data.get("state_iso")
    city_name = geo_data.get("city_name")

    data = {
        "event_time": event_time,
        DB_NETWORK: source,
        DB_STORE_ID: app,
        DB_C: c,
        DB_C_ID: c_id,
        DB_AD_NAME: ad,
        DB_AD_ID: ad_id,
        DB_IFA: ifa,
        DB_CLIENT_IP: client_host,
        DB_LINK_UID: link_uid,
        DB_COUNTRY_ISO: country_iso,
        DB_STATE_ISO: state_iso,
        DB_CITY_NAME: city_name,
        DB_RECEIVED_AT: now(),
    }

    try:
        enc_data = json.dumps(data).encode("utf-8")
        CLICK_PRODUCER.produce("impressions", value=enc_data)
        CLICK_PRODUCER.poll(0)
    except KafkaException as ex:
        logger.exception("Write to Kafka Impressions failed.")
        raise HTTPException(status_code=500, detail=ex.args[0].str()) from ex


class ShareController(Controller):
    """
    Recording for share endpoints.

    Endpoints for Share Links
    =========
    /s

    """

    path = "s"

    @get(path="{share_slug:str}")
    async def shared_link(
        self: Self,
        request: Request,
        share_slug: str,
    ) -> None:
        """
        Record clicks on share links.

        URL Path: GET s/{share_slug:str}

        Args:
        ----
            self: not for external use
            request: not for external use
            share_slug (str): The share slug included in the URL path.

        Returns:
        -------
        - None: The function does not return any value.

        Behavior
        --------
        1. Extracts the client's host information from the request.
        2. Constructs a data dictionary with the provided parameters and additional information like the client's IP address.
        3. Serializes the data dictionary into a JSON string and encodes it to UTF-8.
        4. Produces a message with the encoded data to the "impressions" Kafka topic.


        Example Usage
        -------------
        ```
        GET https://track.example.com/s/abc
        ```

        """
        link_uid = generate_link_uid()

        # TODO: move this to process_share_link?
        client_host = get_client_ip(request)

        if is_android_device(request):
            redirect_url = APP_LINKS[share_slug]["google_redirect"]
        elif is_ios_device(request):
            redirect_url = APP_LINKS[share_slug]["apple_redirect"]
        else:
            # TODO: Needs a web landing page
            raise HTTPException(status_code=400, detail="Unsupported device")

        return RedirectResponse(
            url=redirect_url,
            background=BackgroundTask(
                process_share_link,
                share_slug,
                client_host,
                link_uid,
            ),
        )

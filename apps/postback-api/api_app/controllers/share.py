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
from enum import Enum
from typing import Self

from config import IMPRESSION_CLICK_PRODUCER, get_logger
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
from dbcon.queries import APP_LINKS_DF
from detect.geo import get_geo
from litestar import Controller, Request, get
from litestar.background_tasks import BackgroundTask
from litestar.exceptions import HTTPException
from litestar.response import Redirect
from ua_parser import parse

from api_app.tools import EMPTY_IFA, generate_link_uid, get_client_ip, now

logger = get_logger(__name__)


class OSID(Enum):
    """Enum for store IDs."""

    ANDROID = "android"
    IOS = "ios"
    MACOS = "macos"
    WINDOWS = "windows"


class StoreId(Enum):
    """Enum for store IDs."""

    GOOGLE = "google"
    APPLE = "apple"
    WEB = "web"
    ERROR = "error"


# Define helper functions to determine the device type
def is_android_device(request: Request) -> bool:
    """Determine if the request is from an Android device."""
    user_agent = request.headers.get("User-Agent", "")
    parsed_ua = parse(user_agent)
    return parsed_ua.os.family.lower() == "android"


def is_ios_device(request: Request) -> bool:
    """Determine if the request is from an iOS device."""
    user_agent = request.headers.get("User-Agent", "")
    parsed_ua = parse(user_agent)
    return parsed_ua.os.family.lower() in {"ios", "iphone os"}


def process_share_link(
    share_slug: str,
    request: Request,
    redirected_store_id: StoreId,
) -> None:
    """Process the share link in background."""
    client_host = get_client_ip(request)
    link_uid = generate_link_uid()

    link_data = APP_LINKS_DF[share_slug]

    if redirected_store_id == StoreId.ANDROID and link_data["google_store_id"]:
        app = link_data.get("google_store_id")
    elif redirected_store_id == StoreId.IOS and link_data["apple_store_id"]:
        app = link_data.get("apple_store_id")
    else:
        app = ""

    event_time = now()
    ifa = EMPTY_IFA
    source = link_data.get("network_postback_id")
    c = link_data.get("campaign_name")
    c_id = link_data.get("campaign_id")
    ad = link_data.get("ad_name")
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
        IMPRESSION_CLICK_PRODUCER.produce("clicks", value=enc_data)
        IMPRESSION_CLICK_PRODUCER.poll(0)
    except KafkaException as ex:
        logger.exception("Write share to Kafka Clicks failed.")
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
        Redirect to the store ID's URL based on the device type.

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
        1. Determines the store ID to redirect to based on the device type.
        2. Redirects to the store ID's URL.
        3. Processes the share link in the background as a click event.

        Example Usage
        -------------
        ```
        GET https://track.example.com/s/abc
        ```

        """
        if len(APP_LINKS_DF) == 0:
            logger.error(
                f"Redirect links empty! Set share link on dashboard. No redirect found for {share_slug}",
            )
            return Redirect(path="/")

        if is_android_device(request):
            redirected_store_id = OSID.ANDROID
            try:
                redirect_url = APP_LINKS_DF[share_slug]["google_redirect"]
            except KeyError:
                logger.exception(f"No google redirect found for {share_slug}")
                redirect_url = APP_LINKS_DF[share_slug]["web_redirect"]
                redirected_store_id = StoreId.WEB
        elif is_ios_device(request):
            redirected_store_id = StoreId.APPLE
            try:
                redirect_url = APP_LINKS_DF[share_slug]["apple_redirect"]
            except KeyError:
                logger.exception(f"No apple redirect found for {share_slug}")
                redirect_url = APP_LINKS_DF[share_slug]["web_redirect"]
                redirected_store_id = StoreId.WEB
        else:
            logger.error(f"No redirect found for {share_slug}")
            try:
                redirect_url = APP_LINKS_DF[share_slug]["web_redirect"]
                redirected_store_id = StoreId.WEB
            except KeyError:
                logger.exception(f"No web redirect found for {share_slug}")
                redirected_store_id = StoreId.ERROR
                return Redirect(
                    path="/",
                    background=BackgroundTask(
                        process_share_link,
                        share_slug,
                        request,
                        redirected_store_id,
                    ),
                )

        return Redirect(
            path=redirect_url,
            background=BackgroundTask(
                process_share_link,
                share_slug,
                request,
                redirected_store_id,
            ),
        )

"""
API endpoints for postbacks from both in-app and ad networks.

Endpoints for Ad Networks
=========
/collect/impressions/
/collect/clicks/

Endpoints for In App Events
=========
/collect/events/

Endpoint for Health Check
=========
/health

"""

from typing import Annotated, Self

from config import get_logger
from config.dimensions import (
    APP_EVENT_ID,
    APP_EVENT_REV,
    APP_EVENT_TIME,
    DB_AD_ID,
    DB_AD_NAME,
    DB_C,
    DB_C_ID,
    DB_CITY_NAME,
    DB_CLIENT_IP,
    DB_COUNTRY_ISO,
    DB_EVENT_UID,
    DB_IFA,
    DB_LINK_UID,
    DB_NETWORK,
    DB_OA_UID,
    DB_RECEIVED_AT,
    DB_STATE_ISO,
    DB_STORE_ID,
    LINK_AD,
    LINK_AD_ID,
    LINK_CAMPAIGN,
    LINK_CAMPAIGN_ID,
    LINK_EVENT_TIME,
    LINK_IFA,
    LINK_NETWORK,
    LINK_UID,
)
from detect.geo import get_geo
from litestar import Controller, Request, get, post
from litestar.exceptions import HTTPException
from litestar.params import Parameter

from api_app.models import ClickData, EventData, ImpressionData, RequestEventData
from api_app.sendkafka import to_kafka
from api_app.tools import EMPTY_IFA, get_client_ip, is_valid_ifa, is_valid_uuid, now

logger = get_logger(__name__)


class PostbackController(Controller):
    """
    Record all postback endpoints.

    Endpoints for Ad Networks
    =========
    collect/impressions/
    collect/clicks/

    Endpoints for In App Events
    =========
    collect/events/

    """

    path = "collect"

    @get(path="impressions/{app:str}")
    async def impressions(
        self: Self,
        request: Request,
        app: str,
        source: Annotated[str, Parameter(str, query=LINK_NETWORK)],
        c: Annotated[str, Parameter(str, query=LINK_CAMPAIGN)],
        event_time: Annotated[int, Parameter(int, query=LINK_EVENT_TIME)],
        link_uid: Annotated[str, Parameter(str, query=LINK_UID)],
        c_id: Annotated[
            str | None,
            Parameter(str, query=LINK_CAMPAIGN_ID, required=False),
        ] = None,
        ad: Annotated[str | None, Parameter(str, query=LINK_AD, required=False)] = None,
        ad_id: Annotated[
            str | None,
            Parameter(str, query=LINK_AD_ID, required=False),
        ] = None,
        ifa: Annotated[
            str | None,
            Parameter(str, query=LINK_IFA, required=False),
        ] = None,
    ) -> None:
        """
        Record impression postbacks for app from an ad network.

        Process various query parameters related to the impression, such as the source network, campaign details, event time, and other identifiers. The data is then serialized and sent to a Kafka topic named "impressions".

        URL Path: GET collect/impressions/{app:str}

        Args:
        ----
            self: not for external use
            request: not for external use
            app (str): The application identifier included in the URL path.
            source (str): The source network for the impression. Obtained from query parameter LINK_NETWORK.
            c (str): The campaign name associated with the impression. Obtained from query parameter LINK_CAMPAIGN.
            event_time (int): The time of the event associated with the impression. Obtained from query parameter LINK_EVENT_TIME.
            link_uid (str): A unique identifier for the link. Obtained from query parameter LINK_UID.
            c_id (str, optional): The campaign ID. Obtained from query parameter LINK_CAMPAIGN_ID. Default is None.
            ad (str, optional): The name of the advertisement. Obtained from query parameter LINK_AD. Default is None.
            ad_id (str, optional): The advertisement ID. Obtained from query parameter LINK_AD_ID. Default is None.
            ifa (str, optional): Identifier for Advertisers. Obtained from query parameter LINK_IFA. Default is None.

        Returns:
        -------
        - None: The function does not return any value.

        Behavior
        --------
        1. Extracts the client's host information from the request.
        2. Constructs a data dictionary with the provided parameters and additional information like the client's IP address.
        3. Serializes the data dictionary into a JSON string and encodes it to UTF-8.
        4. Produces a message with the encoded data to the "impressions" Kafka topic.
        5. Handles any KafkaException by logging an error message and raising an HTTPException.

        Exceptions
        ----------
        - HTTPException: Raised if an error occurs while producing the message to the Kafka topic.

        Example Usage
        -------------
        ```
        GET https://track.example.com/collect/impressions/com.example.app?source_network=abc&campaign=xyz&event_time=1617715200&link_uid=123&campaign_id=456&ad_name=ad_sample&ad_id=789&ifa=ifa_value
        ```

        """
        client_host = get_client_ip(request)

        if not is_valid_ifa(ifa):
            raise HTTPException(
                status_code=400,
                detail="Invalid ifa format, use a v4 UUID",
            )
        if not is_valid_uuid(link_uid):
            raise HTTPException(
                status_code=400,
                detail="Invalid link_uid format, use a v4 UUID",
            )

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

        impression = ImpressionData(**data)

        to_kafka(impression, "impressions")

    @get(path="clicks/{app:str}")
    async def clicks(
        self: Self,
        request: Request,
        app: str,
        source: Annotated[str, Parameter(str, query=LINK_NETWORK)],
        c: Annotated[str, Parameter(str, query=LINK_CAMPAIGN)],
        event_time: Annotated[int, Parameter(int, query=LINK_EVENT_TIME)],
        link_uid: Annotated[str, Parameter(str, query=LINK_UID)],
        c_id: Annotated[
            str | None,
            Parameter(str, query=LINK_CAMPAIGN_ID, required=False),
        ] = None,
        ad: Annotated[str | None, Parameter(str, query=LINK_AD, required=False)] = None,
        ad_id: Annotated[
            str | None,
            Parameter(str, query=LINK_AD_ID, required=False),
        ] = None,
        ifa: Annotated[
            str | None,
            Parameter(str, query=LINK_IFA, required=False),
        ] = None,
    ) -> None:
        """
        Record click postbacks for app from an ad network.

        Process various query parameters related to the impression, such as the source network, campaign details, event time, and other identifiers. The data is then serialized and sent to a Kafka topic named "impressions".

        URL Path: GET collect/clicks/{app:str}

        Args:
        ----
          app (str): The application identifier included in the URL path.
          source (str): The source network for the impression. Obtained from query parameter LINK_NETWORK.
          c (str): The campaign name associated with the impression. Obtained from query parameter LINK_CAMPAIGN.
          event_time (int): The time of the event associated with the impression. Obtained from query parameter LINK_EVENT_TIME.
          link_uid (str): A unique identifier for the link. Obtained from query parameter LINK_UID.
          c_id (str, optional): The campaign ID. Obtained from query parameter LINK_CAMPAIGN_ID. Default is None.
          ad (str, optional): The name of the advertisement. Obtained from query parameter LINK_AD. Default is None.
          ad_id (str, optional): The advertisement ID. Obtained from query parameter LINK_AD_ID. Default is None.
          ifa (str, optional): Identifier for Advertisers. Obtained from query parameter LINK_IFA. Default is None.
          self: not for external use.
          request: not for external use.

        Returns:
        -------
        - None: The function does not return any value.

        Behavior
        --------
        1. Extracts the client's host information from the request.
        2. Constructs a data dictionary with the provided parameters and additional information like the client's IP address.
        3. Serializes the data dictionary into a JSON string and encodes it to UTF-8.
        4. Produces a message with the encoded data to the "impressions" Kafka topic.
        5. Handles any KafkaException by logging an error message and raising an HTTPException.

        Exceptions
        ----------
        - HTTPException: Raised if an error occurs while producing the message to the Kafka topic.

        Example Usage
        -------------
        ```
        GET https://track.example.com/collect/clicks/com.example.app?source_network=abc&campaign=xyz&event_time=1617715200&link_uid=123&campaign_id=456&ad_name=ad_sample&ad_id=789&ifa=ifa_value
        ```

        """
        client_host = get_client_ip(request)

        if not is_valid_ifa(ifa):
            raise HTTPException(
                status_code=400,
                detail="Invalid ifa format, use a v4 UUID",
            )
        if not is_valid_uuid(link_uid):
            raise HTTPException(
                status_code=400,
                detail="Invalid link_uid format, use a v4 UUID",
            )

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
        click = ClickData(**data)

        to_kafka(click, "clicks")

    @post(path="events/{app:str}")
    async def events(
        self: Self,
        request: Request,
        app: str,
        data: RequestEventData,
    ) -> None:
        """
        Record event postbacks from in app.

        Process various query parameters related to the in app events, such as the event_id, event_time and user's ifa

        URL Path: GET collect/events/{app:str}

        Args:
        ----
          app (str): The iOS or Android Store ID. Examples: 123456789 or com.example.app.
          request: not for external use.
          data: RequestEventData
            {
            event_id (str): The sting ID for an event tracked. Examples: 'tutorial', 'level_1'
            event_time (int): The time of the event associated with the impression. Obtained from query parameter LINK_EVENT_TIME.
            event_uid (str): A unique generated UID for the event, this is used for deduplication.
            ifa (str, optional): Identifier for Advertisers.
            revenue (str, optional): The numerical value of the revenue in USD. Examples: '1', '1.00', '0.222'
            oa_uid (str): The unique ID for the user generated by the OpenAttribution SDK.
            }


        Returns:
        -------
        - None: The function does not return any value.

        Behavior
        --------
        1. Extracts the client's host information from the request.
        2. Constructs a data dictionary with the provided parameters and additional information like the client's IP address.
        3. Serializes the data dictionary into a JSON string and encodes it to UTF-8.
        4. Produces a message with the encoded data to the "events" Kafka topic.
        5. Handles any KafkaException by logging an error message and raising an HTTPException.

        Exceptions
        ----------
        - HTTPException: Raised if an error occurs while producing the message to the Kafka topic.

        Example Usage
        -------------
        ```
        GET https://track.example.com/collect/events/com.example.app?event_id=level_1&event_time=1706499131&oa_uid=6a660ee7-bbc1-4440-9fdd-6564aca3560c&event_uid=6a660ee7-bbc1-4440-9fdd-6564aca3560c
        ```

        """
        client_host = get_client_ip(request)
        ifa = data.ifa
        if not is_valid_ifa(ifa):
            if ifa is None:
                ifa = EMPTY_IFA
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid ifa format, use a v4 UUID",
                )
        if not is_valid_uuid(data.event_uid):
            raise HTTPException(
                status_code=400,
                detail="Invalid event_uid format, use a v4 UUID",
            )
        if not is_valid_uuid(data.oa_uid):
            raise HTTPException(
                status_code=400,
                detail="Invalid oa_uid format, use a v4 UUID",
            )

        geo_data = get_geo(client_host)
        country_iso = geo_data.get("country_iso")
        state_iso = geo_data.get("state_iso")
        city_name = geo_data.get("city_name")

        data = {
            DB_STORE_ID: app,
            APP_EVENT_ID: data.event_id,
            APP_EVENT_TIME: data.event_time,
            DB_IFA: ifa,
            APP_EVENT_REV: data.revenue,
            DB_CLIENT_IP: client_host,
            DB_OA_UID: data.oa_uid,
            DB_EVENT_UID: data.event_uid,
            DB_COUNTRY_ISO: country_iso,
            DB_STATE_ISO: state_iso,
            DB_CITY_NAME: city_name,
            DB_RECEIVED_AT: now(),
        }
        event = EventData(**data)
        to_kafka(event, "events")

    @get(path="health")
    async def health(self: Self) -> dict:
        """Health check endpoint for the postback API."""
        return {"status": "ok"}

"""
API endpoints for postbacks from both in-app and ad networks.

Endpoints for Ad Networks
=========
/collect/impressions/
/collect/clicks/

Endpoints for In App Events
=========
/collect/events/

"""

import datetime
import json
from typing import Annotated, Self

from config import KAFKA_LOCATION, get_logger
from config.dimensions import (
    APP_EVENT_ID,
    APP_EVENT_REV,
    APP_EVENT_TIME,
    APP_EVENT_UID,
    DB_AD_ID,
    DB_AD_NAME,
    DB_C,
    DB_C_ID,
    DB_CLIENT_IP,
    DB_EVENT_UID,
    DB_IFA,
    DB_LINK_UID,
    DB_NETWORK,
    DB_RECEIVED_AT,
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
from confluent_kafka import KafkaException, Producer
from litestar import Controller, Request, get
from litestar.exceptions import HTTPException
from litestar.params import Parameter

logger = get_logger(__name__)


# If inside docker: "bootstrap.servers": "kafka:9093",
reg_config = {
    "bootstrap.servers": KAFKA_LOCATION,
}

event_config = {
    "bootstrap.servers": KAFKA_LOCATION,
    "linger.ms": 1000,  # This is to attempt to slow down events to allow clickhouse mv to process clicks. Should be handled some other way in ClickHouse?
}
reg_producer = Producer(reg_config)
event_producer = Producer(event_config)


def now() -> str:
    """Return datetime in epoch milliseconds as integer."""
    timestamp_with_ms_int = str(
        int(datetime.datetime.now(datetime.UTC).timestamp() * 1000),
    )
    return timestamp_with_ms_int


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
        client_host = request.client.host

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
            DB_RECEIVED_AT: now(),
        }

        try:
            enc_data = json.dumps(data).encode("utf-8")
            reg_producer.produce("impressions", value=enc_data)
            reg_producer.poll(0)
        except KafkaException as ex:
            logger.exception("Write to Kafka Impressions failed.")
            raise HTTPException(status_code=500, detail=ex.args[0].str()) from ex

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
        client_host = request.client.host

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
            DB_RECEIVED_AT: now(),
        }

        try:
            enc_data = json.dumps(data).encode("utf-8")
            reg_producer.produce("clicks", value=enc_data)
            reg_producer.poll(0)
        except KafkaException as ex:
            logger.exception("Process click for kafka failed.")
            raise HTTPException(status_code=500, detail=ex.args[0].str()) from ex

    @get(path="events/{app:str}")
    async def events(
        self: Self,
        request: Request,
        app: str,
        event_id: Annotated[str, Parameter(str, query=APP_EVENT_ID)],
        event_time: Annotated[int, Parameter(int, query=APP_EVENT_TIME)],
        event_uid: Annotated[str, Parameter(str, query=APP_EVENT_UID)],
        ifa: Annotated[
            str | None,
            Parameter(str, query=LINK_IFA, required=False),
        ] = None,
        revenue: Annotated[
            str | None,
            Parameter(str, query=APP_EVENT_REV, required=False),
        ] = None,
    ) -> None:
        """
        Record event postbacks from in app.

        Process various query parameters related to the in app events, such as the event_id, event_time and user's ifa

        URL Path: GET collect/events/{app:str}

        Args:
        ----
          app (str): The iOS or Android Store ID. Examples: 123456789 or com.example.app.
          event_id (str): The sting ID for an event tracked. Examples: 'tutorial', 'level_1'
          event_time (int): The time of the event associated with the impression. Obtained from query parameter LINK_EVENT_TIME.
          event_uid (str): A unique generated UID for the event, this is used for deduplication.
          ifa (str, optional): Identifier for Advertisers.
          revenue (str, optional): The numerical value of the revenue in USD. Examples: '1', '1.00', '0.222'
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
        GET https://track.example.com/collect/events/com.example.app?event_id=level_1&event_time=1706499131&&event_uid=6a660ee7-bbc1-4440-9fdd-6564aca3560c
        ```

        """
        client_host = request.client.host

        data = {
            DB_STORE_ID: app,
            APP_EVENT_ID: event_id,
            APP_EVENT_TIME: event_time,
            DB_IFA: ifa,
            APP_EVENT_REV: revenue,
            DB_CLIENT_IP: client_host,
            DB_EVENT_UID: event_uid,
            DB_RECEIVED_AT: now(),
        }

        try:
            enc_data = json.dumps(data).encode("utf-8")
            event_producer.produce("events", value=enc_data)
            event_producer.poll(0)
        except KafkaException as ex:
            logger.exception("Processing event postback for kafka failed")
            raise HTTPException(status_code=500, detail=ex.args[0].str()) from ex

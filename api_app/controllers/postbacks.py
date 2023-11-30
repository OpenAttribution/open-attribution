import json
from typing import Annotated

from confluent_kafka import KafkaException, Producer
from litestar import Controller, Request, get
from litestar.exceptions import HTTPException
from litestar.params import Parameter

from config import get_logger
from config.dimensions import (
    APP_EVENT_ID,
    APP_EVENT_REV,
    APP_EVENT_TIME,
    DB_AD_ID,
    DB_AD_NAME,
    DB_C,
    DB_C_ID,
    DB_CLIENT_IP,
    DB_IFA,
    DB_NETWORK,
    DB_STORE_ID,
    LINK_AD,
    LINK_AD_ID,
    LINK_CAMPAIGN,
    LINK_CAMPAIGN_ID,
    LINK_EVENT_TIME,
    LINK_IFA,
    LINK_NETWORK,
)

logger = get_logger(__name__)

"""
/impressions/
/clicks/
"""

pconfig = {"bootstrap.servers": "localhost:9092"}
producer = Producer(pconfig)


class PostbackController(Controller):
    path = "collect"

    @get(path="impressions/{app:str}")
    async def impressions(
        self,
        request: Request,
        app: str,
        source: Annotated[str, Parameter(str, query=LINK_NETWORK)],
        c: Annotated[str, Parameter(str, query=LINK_CAMPAIGN)],
        c_id: Annotated[
            str | None, Parameter(str, query=LINK_CAMPAIGN_ID, required=False)
        ] = None,
        ad: Annotated[str | None, Parameter(str, query=LINK_AD, required=False)] = None,
        ad_id: Annotated[
            str | None, Parameter(str, query=LINK_AD_ID, required=False)
        ] = None,
        ifa: Annotated[
            str | None, Parameter(str, query=LINK_IFA, required=False)
        ] = None,
    ) -> None:
        """
        Handles a GET request for a list of apps

        Args:
            app:app

        Returns:
            A dictionary representation of the list of apps for homepage
        """
        logger.info(f"{self.path} start")

        client_host = request.client.host

        data = {
            DB_NETWORK: source,
            DB_STORE_ID: app,
            DB_C: c,
            DB_C_ID: c_id,
            DB_AD_NAME: ad,
            DB_AD_ID: ad_id,
            DB_IFA: ifa,
            DB_CLIENT_IP: client_host,
        }

        try:
            enc_data = json.dumps(data).encode("utf-8")
            producer.produce("impressions", value=enc_data)
            producer.poll(0)
            logger.info("kafka insert success!")
        except KafkaException as ex:
            logger.error({"status": "error", "message": str(ex)})
            raise HTTPException(status_code=500, detail=ex.args[0].str()) from ex

    @get(path="clicks/{app:str}")
    async def clicks(
        self,
        request: Request,
        app: str,
        source: Annotated[str, Parameter(str, query=LINK_NETWORK)],
        c: Annotated[str, Parameter(str, query=LINK_CAMPAIGN)],
        c_id: Annotated[
            str | None, Parameter(str, query=LINK_CAMPAIGN_ID, required=False)
        ] = None,
        ad: Annotated[str | None, Parameter(str, query=LINK_AD, required=False)] = None,
        ad_id: Annotated[
            str | None, Parameter(str, query=LINK_AD_ID, required=False)
        ] = None,
        ifa: Annotated[
            str | None, Parameter(str, query=LINK_IFA, required=False)
        ] = None,
        event_time: Annotated[str | None, Parameter(int, query=LINK_EVENT_TIME)] = None,
    ) -> None:
        """
        Handles a GET request for a list of apps

        Args:
            app:app

        Returns:
            A dictionary representation of the list of apps for homepage
        """
        logger.info(f"{self.path} start")

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
        }

        try:
            enc_data = json.dumps(data).encode("utf-8")
            producer.produce("clicks", value=enc_data)
            producer.poll(0)
            logger.info("kafka insert success!")
        except KafkaException as ex:
            logger.error({"status": "error", "message": str(ex)})
            raise HTTPException(status_code=500, detail=ex.args[0].str()) from ex

    @get(path="events/{app:str}")
    async def events(
        self,
        request: Request,
        app: str,
        event_id: Annotated[str, Parameter(str, query=APP_EVENT_ID)],
        event_time: Annotated[str, Parameter(str, query=APP_EVENT_TIME)],
        ifa: Annotated[
            str | None, Parameter(str, query=LINK_IFA, required=False)
        ] = None,
        revenue: Annotated[
            str | None, Parameter(str, query=APP_EVENT_REV, required=False)
        ] = None,
    ) -> None:
        """
        Handles a GET request to send postback for an app install, event or revenue

        Args:
            app:app

        Returns:
            A dictionary representation of the list of apps for homepage
        """
        logger.info(f"{self.path} start")

        client_host = request.client.host

        data = {
            DB_STORE_ID: app,
            APP_EVENT_ID: event_id,
            APP_EVENT_TIME: event_time,
            DB_IFA: ifa,
            APP_EVENT_REV: revenue,
            DB_CLIENT_IP: client_host,
        }

        try:
            enc_data = json.dumps(data).encode("utf-8")
            producer.produce("events", value=enc_data)
            producer.poll(0)
            logger.info("kafka insert success!")
        except KafkaException as ex:
            logger.error({"status": "error", "message": str(ex)})
            raise HTTPException(status_code=500, detail=ex.args[0].str()) from ex

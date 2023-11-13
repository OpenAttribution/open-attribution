import json

from confluent_kafka import KafkaException, Producer
from litestar import Controller, Request, get
from litestar.exceptions import HTTPException

from config import get_logger

logger = get_logger(__name__)

"""
/impressions/
/clicks/
"""

pconfig = {"bootstrap.servers": "localhost:9092"}
producer = Producer(pconfig)


class PostbackController(Controller):
    path = "collect"

    @get(path="impression/{app:str}")
    async def impressions(
        self,
        request: Request,
        app: str,
        source: str,
        c: str,
        c_id: str | None = None,
        ad: str | None = None,
        ifa: str | None = None,
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
            "source": source,
            "app": app,
            "campaign_name": c,
            "campaign_id": c_id,
            "ad": ad,
            "client_ip": client_host,
        }

        try:
            enc_data = json.dumps(data).encode("utf-8")
            producer.produce("impressions", value=enc_data)
            producer.poll(0)
            logger.info("insert success!")
        except KafkaException as ex:
            logger.error({"status": "error", "message": str(ex)})
            raise HTTPException(status_code=500, detail=ex.args[0].str()) from ex

    @get(path="click/{app:str}")
    async def clicks(
        self,
        request: Request,
        app: str,
        source: str,
        c: str,
        c_id: str | None = None,
        ad: str | None = None,
        ifa: str | None = None,
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
            "source": source,
            "app": app,
            "campaign_name": c,
            "campaign_id": c_id,
            "ad": ad,
            "client_ip": client_host,
        }

        try:
            enc_data = json.dumps(data).encode("utf-8")
            producer.produce("clicks", value=enc_data)
            producer.poll(0)
            logger.info(f"data={enc_data.decode()} success!")
        except KafkaException as ex:
            logger.error({"status": "error", "message": str(ex)})
            raise HTTPException(status_code=500, detail=ex.args[0].str()) from ex

from litestar import Controller, get
from litestar.exceptions import HTTPException

from confluent_kafka import KafkaException, Producer

import json 






from config import get_logger

logger = get_logger(__name__)

"""
/impressions/
/clicks/
"""

pconfig = {"bootstrap.servers": "localhost:9092"}
producer = Producer(pconfig)



def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))



class PostbackController(Controller):
    path = "/impressions"

    @get(path="/{app:str}")
    async def impressions(self, app: str, c:str, c_id:str | None = None, ad:str | None = None) -> None:
        """
        Handles a GET request for a list of apps

        Args:
            app:app

        Returns:
            A dictionary representation of the list of apps for homepage
        """
        logger.info(f"{self.path} start")


        data = {"app":app, "campaign_name":c, "campaign_id": c_id, "ad":ad}

        try:
            enc_data = json.dumps(data).encode('utf-8')
            logger.info(f'data={enc_data}')
            producer.produce("mytopic", value=enc_data)
            producer.poll(0)
            logger.info(f'data={enc_data} success!')
        except KafkaException as ex:
            logger.error({"status": "error", "message": str(ex)})
            raise HTTPException(status_code=500, detail=ex.args[0].str())


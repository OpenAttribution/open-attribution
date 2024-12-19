"""Send data to kafka."""

import json
from dataclasses import asdict

from config import EVENT_PRODUCER, IMPRESSION_CLICK_PRODUCER, get_logger
from confluent_kafka import KafkaException
from litestar.exceptions import HTTPException

from api_app.models import ClickData, EventData, ImpressionData

logger = get_logger(__name__)


def to_kafka(data: ClickData | ImpressionData | EventData, topic: str) -> None:
    """Send data to kafka."""
    enc_data = json.dumps(asdict(data)).encode("utf-8")
    if topic in ["impressions", "clicks"]:
        try:
            IMPRESSION_CLICK_PRODUCER.produce(topic, value=enc_data)
            IMPRESSION_CLICK_PRODUCER.poll(0)
        except KafkaException as ex:
            logger.exception(f"Write to Kafka topic {topic} failed.")
            raise HTTPException(status_code=500, detail=ex.args[0].str()) from ex
    elif topic == "events":
        try:
            EVENT_PRODUCER.produce(topic, value=enc_data)
            EVENT_PRODUCER.poll(0)
        except KafkaException as ex:
            logger.exception("Write to Kafka Events failed.")
            raise HTTPException(status_code=500, detail=ex.args[0].str()) from ex
    else:
        raise HTTPException(status_code=400, detail="Invalid topic")

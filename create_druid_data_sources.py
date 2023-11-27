import json
import time

import requests

from config import get_logger
from config.dimensions import DB_CLIENT_IP, DB_IFA, MY_SCHEMAS

logger = get_logger(__name__)

DRUID_HOST: str = "http://localhost:8081/druid/indexer/v1/supervisor"


# Define a function to create a Kafka Ingestion Spec for Druid
def stop_kafka_ingest(
    topic_name: str,
) -> None:
    response = requests.post(DRUID_HOST + f"/{topic_name}/shutdown")
    logger.info(f"Druid shutown ingest: {topic_name=} response: {response.status_code}")
    topic_name = f"{topic_name}_stats"
    response_agg = requests.post(DRUID_HOST + f"/{topic_name}/shutdown")
    logger.info(
        f"Druid shutown ingest: {topic_name=} response: {response_agg.status_code}"
    )


# Define a function to create a Kafka Ingestion Spec for Druid
def create_kafka_ingest(
    topic_name: str,
    dimensions: list[str],
    bootstrap_servers: str = "localhost:9092",
) -> None:
    # Create the Kafka Ingestion Spec in JSON format
    raw_data_schema = {
        "dataSource": topic_name,
        "timestampSpec": {"column": "kafka.timestamp", "format": "millis"},
        "dimensionsSpec": {"dimensions": dimensions},
        "granularitySpec": {
            "queryGranularity": "none",
            "rollup": False,
            "segmentGranularity": "day",
        },
    }
    agg_data_schema = {
        "dataSource": topic_name + "_stats",
        "timestampSpec": {"column": "kafka.timestamp", "format": "millis"},
        "dimensionsSpec": {
            "dimensions": [x for x in dimensions if x not in [DB_CLIENT_IP, DB_IFA]],
        },
        "granularitySpec": {
            "queryGranularity": "hour",
            "rollup": True,
            "segmentGranularity": "day",
        },
        "metricsSpec": [{"name": "count", "type": "count"}],
    }
    raw_kafka_ingestion_spec = json.dumps(
        {
            "type": "kafka",
            "spec": {
                "ioConfig": {
                    "type": "kafka",
                    "consumerProperties": {"bootstrap.servers": bootstrap_servers},
                    "topic": topic_name,
                    "inputFormat": {"type": "kafka", "valueFormat": {"type": "json"}},
                    "useEarliestOffset": True,
                },
                "tuningConfig": {
                    "type": "kafka",
                    "resetOffsetAutomatically": True,
                },
                "dataSchema": raw_data_schema,
            },
        }
    )
    agg_kafka_ingestion_spec = json.dumps(
        {
            "type": "kafka",
            "spec": {
                "ioConfig": {
                    "type": "kafka",
                    "consumerProperties": {"bootstrap.servers": bootstrap_servers},
                    "topic": topic_name,
                    "inputFormat": {"type": "kafka", "valueFormat": {"type": "json"}},
                    "useEarliestOffset": True,
                },
                "tuningConfig": {
                    "type": "kafka",
                    "resetOffsetAutomatically": True,
                },
                "dataSchema": agg_data_schema,
            },
        }
    )
    # Set headers for the post request
    headers = {"Content-Type": "application/json"}

    try:
        # Make a post request to Druid with the Kafka ingestion spec
        response = requests.post(DRUID_HOST, raw_kafka_ingestion_spec, headers=headers)
        # Raise an exception if the request was unsuccessful
        response.raise_for_status()
        logger.info(
            f"Druid create ingest: {topic_name=} response: {response.status_code} {response.text}"
        )
        response_agg = requests.post(
            DRUID_HOST, agg_kafka_ingestion_spec, headers=headers
        )
        # Aggregated create
        response_agg.raise_for_status()
        logger.info(
            f"Druid create ingest: {topic_name=} response: {response_agg.status_code} {response_agg.text}"
        )
    except Exception as e:
        logger.info(
            f"Druid create ingest: {topic_name=} something wrong with request:", e
        )


if __name__ == "__main__":
    for topic, dimensions in MY_SCHEMAS.items():
        stop_kafka_ingest(topic_name=topic)
        create_kafka_ingest(topic_name=topic, dimensions=dimensions)
        time.sleep(2)

import json
import time

import requests

from config.dimensions import DB_CLIENT_IP, DB_IFA, MY_SCHEMAS


# Define a function to create a Kafka Ingestion Spec for Druid
def create_kafka_ingest(
    topic_name: str,
    dimensions: list[str],
    bootstrap_servers: str = "localhost:9092",
    druid_host: str = "http://localhost:8081/druid/indexer/v1/supervisor",
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
                "tuningConfig": {"type": "kafka"},
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
                "tuningConfig": {"type": "kafka"},
                "dataSchema": agg_data_schema,
            },
        }
    )
    # Set headers for the post request
    headers = {"Content-Type": "application/json"}

    print(f"Creating Kafka ingestion spec for {topic_name}")
    try:
        # Make a post request to Druid with the Kafka ingestion spec
        kafka_supervisor_post = requests.post(
            druid_host, raw_kafka_ingestion_spec, headers=headers
        )
        # Raise an exception if the request was unsuccessful
        kafka_supervisor_post.raise_for_status()
        print(kafka_supervisor_post.text)
        kafka_supervisor_post = requests.post(
            druid_host, agg_kafka_ingestion_spec, headers=headers
        )
        kafka_supervisor_post.raise_for_status()
        print(kafka_supervisor_post.text)
    except Exception as e:
        print("Something went wrong with the request:", e)


if __name__ == "__main__":
    for topic, dimensions in MY_SCHEMAS.items():
        create_kafka_ingest(topic_name=topic, dimensions=dimensions)
        time.sleep(2)

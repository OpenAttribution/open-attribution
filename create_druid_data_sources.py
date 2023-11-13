import json
import requests

SHARED_DIMENSIONS = [
          "app",
		  "source",
          "campaign_name",
          "campaign_id"
          "ad_name",
          "ad_id",
		      "advertising_id",
          "client_ip",
        ]


# Define a function to create a Kafka Ingestion Spec for Druid
def create_kafka_ingest(topic_name:str, bootstrap_servers:str='localhost:9092', druid_host:str='http://localhost:8081/druid/indexer/v1/supervisor') -> None:
    # Create the Kafka Ingestion Spec in JSON format
    kafka_ingestion_spec = json.dumps({
  "type": "kafka",
  "spec": {
    "ioConfig": {
      "type": "kafka",
      "consumerProperties": {
        "bootstrap.servers": bootstrap_servers
      },
      "topic": topic_name,
      "inputFormat": {
        "type": "kafka",
        "valueFormat": {
          "type": "json"
        }
      },
      "useEarliestOffset": True
    },
    "tuningConfig": {
      "type": "kafka"
    },
    "dataSchema": {
      "dataSource": topic_name,
      "timestampSpec": {
        "column": "kafka.timestamp",
        "format": "millis"
      },
      "dimensionsSpec": {
        "dimensions":  SHARED_DIMENSIONS
      },
      "granularitySpec": {
        "queryGranularity": "none",
        "rollup": False,
        "segmentGranularity": "day"
      }
    }
  }
    }
    )
	# Set headers for the post request
    headers = {
    	'Content-Type': 'application/json'
    }

    print(f'Creating Kafka ingestion spec for {topic_name}')
    print(f'using this ingestion spec:\n{kafka_ingestion_spec}')
    try:
        # Make a post request to Druid with the Kafka ingestion spec
        kafka_supervisor_post = requests.post(druid_host, kafka_ingestion_spec, headers=headers)
        # Raise an exception if the request was unsuccessful
        kafka_supervisor_post.raise_for_status()
    except Exception as e:
        print("Something went wrong with the request:", e)

    # Print the response
    print(kafka_supervisor_post.text)

if __name__ == '__main__':
    my_topics = ['impressions', 'clicks']
    for topic in my_topics:
        create_kafka_ingest(topic_name=topic)

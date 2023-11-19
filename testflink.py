from dataclasses import dataclass

from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer, KafkaConfig
from pyflink.table import StreamTableEnvironment


# https://github.com/josephmachado/beginner_de_project_stream/blob/ce26ac0aa07c9bffc21c02969002170cc128738b/code/checkout_attribution.py#L27
@dataclass(frozen=True)
class ClickTopicConfig(KafkaConfig):
    topic: str = "clicks"
    format: str = "json"


env = StreamExecutionEnvironment.get_execution_environment()
env.set_stream_time_characteristic(TimeCharacteristic.EventTime)

# Table environment
t_env = StreamTableEnvironment.create(env)


# the sql connector for kafka is used here as it's a fat jar and could avoid dependency issues
env.add_jars("file:///home/james/test-flink/flink-sql-connector-kafka-3.0.1-1.18.jar")

kafka_consumer = FlinkKafkaConsumer(
    topics="impressions",
    deserialization_schema=SimpleStringSchema(),
    properties={"bootstrap.servers": "localhost:9092"},
)

ds = env.add_source(kafka_consumer)

ds.print(sink_identifier="hi: ")


env.execute()

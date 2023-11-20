from dataclasses import dataclass

from pyflink.common.serialization import SimpleStringSchema
from pyflink.common.typeinfo import Types
from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer
from pyflink.table import StreamTableEnvironment


@dataclass(frozen=True)
class KafkaConfig:
    connector: str = "kafka"
    bootstrap_servers: str = "localhost:9092"
    scan_startup_mode: str = "earliest-offset"
    consumer_group_id: str = "flink-consumer-group-1"


# https://github.com/josephmachado/beginner_de_project_stream/blob/ce26ac0aa07c9bffc21c02969002170cc128738b/code/checkout_attribution.py#L27
@dataclass(frozen=True)
class ImpressionTopicConfig(KafkaConfig):
    topic: str = "impressions"
    format: str = "json"


print("stream env start")
env = StreamExecutionEnvironment.get_execution_environment()
env.set_stream_time_characteristic(TimeCharacteristic.EventTime)


print("stream env set")
# Table environment
print("stream table env start")
t_env = StreamTableEnvironment.create(env)

print("stream table env set")


# the sql connector for kafka is used here as it's a fat jar and could avoid dependency issues
env.add_jars("file:///home/james/test-flink/flink-sql-connector-kafka-3.0.1-1.18.jar")

print("create kafka connector")
imp_kafka_consumer = FlinkKafkaConsumer(
    topics="impressions",
    deserialization_schema=SimpleStringSchema(),
    properties={"bootstrap.servers": "localhost:9092"},
)
evt_kafka_consumer = FlinkKafkaConsumer(
    topics="events",
    deserialization_schema=SimpleStringSchema(),
    properties={"bootstrap.servers": "localhost:9092"},
)
print("create kafka connector done")

print("stream env connector add_source")
imp_ds = env.add_source(imp_kafka_consumer)
evt_ds = env.add_source(evt_kafka_consumer)

imp_ds.print(sink_identifier="impression: ")
evt_ds.print(sink_identifier="event: ")

## Define your configuration values
# config_values = {
#    "connector": "kafka",
#    "topic": "impressions",
#    "bootstrap_servers": "localhost:9092",
#    "consumer_group_id": "group1",
#    "scan_startup_mode": "earliest-offset",
#    "format": "json",
# }
#
## Read and format the SQL file
# with open("pyflink_impressions.sql") as file:
#    sql_template = file.read()
#    impressions_table_sql = sql_template.format(**config_values)
# t_env.execute_sql(impressions_table_sql)

import pandas as pd
from pydruid.db import connect

# Establish a connection to Druid
conn = connect(host="localhost", port=8082, path="/druid/v2/sql/", scheme="http")

# Read and format the SQL file
with open("druid_query_impressions.sql") as file:
    sql_query = file.read()

df = pd.read_sql(sql_query, con=conn)

impressions_table = t_env.from_pandas(df)
imp_type_info = Types.ROW(
    [
        Types.STRING(),
        Types.STRING(),
        Types.STRING(),
        Types.STRING(),
        Types.STRING(),
        Types.STRING(),
        Types.STRING(),
        Types.STRING(),
        Types.STRING(),
    ]
)


ds_hist_imps = t_env.to_append_stream(impressions_table, type_info=imp_type_info)

imp_ds = imp_ds.union(ds_hist_imps)


print("executed table create")

env.execute()

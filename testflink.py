from dataclasses import dataclass

import pandas as pd
from pydruid.db import connect
from pyflink.common.serialization import SimpleStringSchema
from pyflink.common.typeinfo import Types
from pyflink.table.descriptors import Schema
from pyflink.table import DataTypes
from pyflink.table.udf import udf
from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
from pyflink.datastream.connectors.hybrid_source import HybridSource
from pyflink.datastream.connectors.kafka import (
    FlinkKafkaConsumer,
    KafkaOffsetsInitializer,
    KafkaSource,
)
from pyflink.table import StreamTableEnvironment

# Establish a connection to Druid
conn = connect(host="localhost", port=8082, path="/druid/v2/sql/", scheme="http")

# Read and format the SQL file
with open("druid_query_impressions.sql") as file:
    sql_query = file.read()


imp_df = pd.read_sql(sql_query, con=conn)

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
# the sql connector for kafka is used here as it's a fat jar and could avoid dependency issues
env.add_jars("file:///home/james/test-flink/flink-sql-connector-kafka-3.0.1-1.18.jar")


print("stream table env start")
t_env = StreamTableEnvironment.create(env)


# Define the schema for the Flink table, matching the structure of the pandas DataFrame
# If __time represents a timestamp, you can use DataTypes.TIMESTAMP(3)
# Otherwise, use DataTypes.STRING() if it's a string representation of the time
table_schema = DataTypes.ROW([
    DataTypes.FIELD("__time", DataTypes.STRING()),  # or DataTypes.STRING() if it's not in a timestamp format
    DataTypes.FIELD("store_id", DataTypes.STRING()),
    DataTypes.FIELD("network", DataTypes.STRING()),
    DataTypes.FIELD("campaign_name", DataTypes.STRING()),
    DataTypes.FIELD("campaign_id", DataTypes.STRING()),
    DataTypes.FIELD("ad_name", DataTypes.STRING()),
    DataTypes.FIELD("ad_id", DataTypes.STRING()),
    DataTypes.FIELD("ifa", DataTypes.STRING()),
    DataTypes.FIELD("client_ip", DataTypes.STRING())
])



# Define the schema for the Flink table, matching the structure of the pandas DataFrame
# If __time represents a timestamp, you can use DataTypes.TIMESTAMP(3)
# Otherwise, use DataTypes.STRING() if it's a string representation of the time
table_schema = DataTypes.ROW([
    DataTypes.FIELD("__time", DataTypes.STRING()),  # or DataTypes.STRING() if it's not in a timestamp format
    DataTypes.FIELD("store_id", DataTypes.STRING()),
    DataTypes.FIELD("network", DataTypes.STRING()),
    DataTypes.FIELD("campaign_name", DataTypes.STRING()),
    DataTypes.FIELD("campaign_id", DataTypes.STRING()),
    DataTypes.FIELD("ad_name", DataTypes.STRING()),
    DataTypes.FIELD("ad_id", DataTypes.STRING()),
    DataTypes.FIELD("ifa", DataTypes.STRING()),
    DataTypes.FIELD("client_ip", DataTypes.STRING())
])




# Define the schema for the Flink table, matching the structure of the pandas DataFrame
historical_impressions_table = t_env.from_pandas(imp_df, schema=table_schema)

print("create kafka connector")
# FlinkKafkaConsumer is for regular streaming
imp_kafka_consumer = FlinkKafkaConsumer(
    topics="impressions",
    deserialization_schema=SimpleStringSchema(),
    properties={"bootstrap.servers": "localhost:9092"},
)


# KafkaSource is for hybrid file+streaming
#impressions_switch_timestamp = int(pd.to_datetime(imp_df.__time.max()).timestamp())
#imp_kafka_consumer = (
#    KafkaSource.builder()
#    .set_bootstrap_servers("localhost:9092")
#    .set_topics("impressions")
#    .set_value_only_deserializer(SimpleStringSchema())
#    .set_starting_offsets(
#        KafkaOffsetsInitializer.timestamp(impressions_switch_timestamp)
#    )
#    .build()
#)


evt_kafka_consumer = FlinkKafkaConsumer(
    topics="events",
    deserialization_schema=SimpleStringSchema(),
    properties={"bootstrap.servers": "localhost:9092"},
)



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

impressions_table = t_env.from_pandas(imp_df)


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



ds_hist_imps = t_env.to_append_stream(historical_impressions_table, type_info=imp_type_info)


# Define a Python function to parse the query string into a Row
@udf(result_type=table_schema)
def parse_query_string(query_str):
    import urllib.parse
    # Parse query string; the leading '&' is ignored by parse_qs
    parsed = urllib.parse.parse_qs(query_str)
    # Extract fields from the parsed query string and return as a tuple
    __time = parsed.get('__time', [None])[0]
    store_id = parsed.get('store_id', [None])[0]
    network = parsed.get('network', [None])[0]
    campaign_name = parsed.get('campaign_name', [None])[0]
    campaign_id = parsed.get('campaign_id', [None])[0]
    ad_name = parsed.get('ad_name', [None])[0]
    ad_id = parsed.get('ad_id', [None])[0]
    ifa = parsed.get('ifa', [None])[0]
    client_ip = parsed.get('client_ip', [None])[0]
    return (__time, store_id, network, campaign_name, campaign_id, ad_name, ad_id, ifa, client_ip)


imp_ds_table = t_env.from_data_stream(imp_ds)

help(t_env.from_data_stream)

parsed_stream = imp_ds.map(parse_query_string)

imp_ds = 

imp_ds.union(parsed_stream)

mycsv = imp_df.to_csv(index=None)


# Using SQL UNION ALL?
"create view t1(s) as values ('c'), ('a'), ('b'), ('b'), ('c');"
"create view t2(s) as values ('d'), ('e'), ('a'), ('b'), ('b');"
"(SELECT s FROM t1) UNION ALL (SELECT s FROM t2);"

# This doesn't work yet
#hybrid_source = HybridSource.builder(mycsv).add_source(imp_kafka_consumer).build()

print("executed table create")

env.execute()

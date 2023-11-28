# These are some of the ways I've tried to imagine the data flow + attribution logic

### Just Druid:
	Device > Python API Endpoint > Kafka > Druid > Superset/frontend
In this simplest flow there was Druid as the raw database. The attribution logic would be handled in materialized views or in stored queries. The problem with this was that it seemed that as data grew the time cost of running queries would have ballooned to be huge.

### Process in Flink idea:
	Device > Python API Endpoint > Kafka > Flink > Druid > Superset/frontend
In this flow the attribution process was going to be handled by Flink, but this turned out to not work due to having to keep a huge amount of data inside Flink to do it. Essentially you would need to store all past attributed installs, 7 days of clicks and 24hrs of impression data in Flink. This itself doesn't seem like too much data, but trying to get this data reliably into Flink seemed to be a point I kept stumbling over. Streaming data from Kafka to flink happens reliably, but mixing this with batch data from db seemed complicated.

### Double DB idea
	Device > Python API Endpoint > Kafka > PostgreSQL > Python Batch Process > Druid > Superset/frontend
This idea would be that the data flows first into PostgreSQL where it can be managed by SQL. The logic for attribution could then be done in batches with Python and inserted into Druid. Huge problem here is the ballooning of resources needed. While some things can be combined to a single server, I think that having PG & Druid on the same system is unlikely at best. This could be substituted for other databases as well like ClickHouse.

### PostgreSQL is all we need?
	Device > Python API Endpoint > Kafka > PostgreSQL > Superset/frontend
Maybe raw data & higher end attribution data and analytics can all be stored into PostgreSQL. This simplifies many things and also importantly keeps the project slim compared to Druid, which is expecting deploys with 16GB of data vs PostgreSQL being happy with 1GB if needed.

### What about ClickHouse?
Since we are going the direction of SQL+Views perhaps we could use ClickHouse since that helps with the frontend serving of OLAP.



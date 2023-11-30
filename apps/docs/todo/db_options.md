

## Druid

pros: 16GB memory is OK
cons: struggling with usage due to materialized views not being available and unclear alternatives

## Pinot

pros: 
- <16GB
- materialized views
- new
cons: 
- struggled to get setup initially?
- new project, less users/examples. Just hit 1.0 Nov 2023
- Warning from their GH page: Pinot is not a replacement for database i.e it cannot be used as source of truth store, cannot mutate data.
- Warning #2: Also, Pinot queries cannot span across multiple tables by default. You can use the [Trino-Pinot Connector](https://trino.io/docs/current/connector/pinot.html) or [Presto-Pinot Connector](https://prestodb.io/docs/current/connector/pinot.html) to achieve table joins and other features.

#### Questions to answer

1. Is my use case considered mutating data?
2. Is my use case well suited for Pinot?

## ClickHouse

pros: materialized views, SQL
cons: 
 - may not operate normally below 16GB RAM
	 - Response: should operate OK below 16GB

## PostgreSQL + TimescaleDB
pros: tiny memory OK
cons: May perform least well at scale
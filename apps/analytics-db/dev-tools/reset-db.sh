#!/bin/bash
sudo docker exec -it clickhouse clickhouse-client --query "DROP DATABASE IF EXISTS default"

# Reset kafka consumer (clickhouse) to rerun data if still in kafka:
sudo docker exec -it kafka kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group clickhouse --reset-offsets --to-earliest --execute --all-topics

# Create database and run startup script
sudo docker exec -it clickhouse clickhouse-client --query "CREATE DATABASE IF NOT EXISTS default"
sudo docker exec -it clickhouse bash /docker-entrypoint-initdb.d/startup.sh

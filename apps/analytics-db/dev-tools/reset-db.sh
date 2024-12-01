#!/bin/bash
sudo docker exec -it clickhouse clickhouse-client --query "DROP DATABASE IF EXISTS default"
sudo docker exec -it clickhouse clickhouse-client --query "CREATE DATABASE IF NOT EXISTS default"
sudo docker exec -it clickhouse bash /docker-entrypoint-initdb.d/startup.sh

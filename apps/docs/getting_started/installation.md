
# Druid

## Druid: Setup

# Kafka

```sh
./bin/kafka-topics.sh --create --topic impressions --bootstrap-server localhost:9092
./bin/kafka-topics.sh --create --topic clicks --bootstrap-server localhost:9092
./bin/kafka-topics.sh --create --topic events --bootstrap-server localhost:9092
```

https://druid.apache.org/docs/latest/tutorials/

## Druid: User (admin)

https://druid.apache.org/docs/latest/operations/security-overview

# Superset

## Superset: Setup

```sh
pip install superset pydruid
export FLASK_APP=superset
export SUPERSET_CONFIG_PATH=superset/superset_config.py
superset db upgrade
superset fab create-admin
```

Setup your username and password for the superset admin login

```sh
superset init
superset run -p 8088 --with-threads --reload
```

1. Add database `druid://admin:password1@localhost:8888/druid/v2/sql`

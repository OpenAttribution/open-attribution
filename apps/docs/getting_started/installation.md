
!!! warning

    This project is very early stage. I am writing the documentation early to help myself plan where the project should be. That means that many features are not yet built and are a work in progress. If you are interested in the project, please feel free to reach out. For now the project is not appropriate for production ad tracking.

# Python environment
Create your python environment for open-attribution using Python 3.11.

The python environment is used for 3 seperate use-cases. If you need you can create individual environments or a single shared environment. Python is used for the Postback API, Kafka & druid setup scripts, Pyflink and the frontend dashboard.

`python3.11 -m venv my-env-path`
`source activate ~/my-env-path/bin/activate`
`pip install pyflink ... `


# Kafka

```sh
./bin/kafka-topics.sh --create --topic impressions --bootstrap-server localhost:9092
./bin/kafka-topics.sh --create --topic clicks --bootstrap-server localhost:9092
./bin/kafka-topics.sh --create --topic events --bootstrap-server localhost:9092
```

https://druid.apache.org/docs/latest/tutorials/

# Druid: User (admin)

Create your druid data sources:
`python create_druid_data_sources.py` 

https://druid.apache.org/docs/latest/operations/security-overview

# Superset

## Superset: Setup
Based on: https://superset.apache.org/docs/installation/installing-superset-from-scratch

Note you'll need go do the configuration to get it running from scratch.

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

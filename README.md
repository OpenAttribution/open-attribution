
# Druid

## Druid: Setup

https://druid.apache.org/docs/latest/tutorials/

## Druid: User (admin)

https://druid.apache.org/docs/latest/operations/security-overview

# Superset

## Superset: Setup

`pip install superset pydruid`

set `export FLASK_APP=superset`
set `export SUPERSET_CONFIG_PATH=superset/superset_config.py`

1. Add database `druid://admin:password1@localhost:8888/druid/v2/sql`

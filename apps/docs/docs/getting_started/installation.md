
!!! warning

    This project is very early stage. I am writing the documentation early to help myself plan where the project should be. That means that many features are not yet built and are a work in progress. If you are interested in the project, please feel free to reach out. For now the project is not appropriate for production ad tracking.



# Docker

While this was originally being built with `bash` and `python` scripts it seems that the more features that were added the less that made sense as a way for different users to deploy. Currently OpenAttribution only supports Docker as a deployment method.


## Installation

```
docker compose -f ~/open-attribution/docker/docker-compose.yml pull
docker compose -f ~/open-attribution/docker/docker-compose.yml up -d
```


This installs several services:

## Services

#### Zookeeper
- Image: `docker.io/bitnami/zookeeper:3.9.2`

#### Kafka
- Image: `docker.io/bitnami/kafka:3.6.2`
- Ports: 9092 (internal), 9093 (external)
- Depends on Zookeeper

#### analytics-db: (ClickHouse)
- Image: `clickhouse/clickhouse-server:24.8.4`
- Ports: 9000, 8123
- Depends on Kafka
- Includes custom init scripts and table creation

#### postback-api
- Image: `openattribution/python-api:main`
- Port: 8000
- Depends on ClickHouse

#### admin-database (PostgreSQL)
- Image: `postgres:17-bullseye`
- contains all user/client data needed for the front end like
	- users: login auth / passwords
	- apps info: name, store_id, icon_url
	- networks: name, postback_id, logo_url
- Includes custom init script

#### dash-backend: (Python)
- Image: `openattribution/dash-backend:main`
- Connects into the `analytics-db` and `admin-db` and handles queries for the frontend. the API is currently internal only and is not meant to be exposed to the outside.
- Port: 8001
- Depends on ClickHouse and Admin DB

#### dash-frontend (Svelte)
- Image: `openattribution/dash-frontend:main`
- This is the user facing admin and analytics dashboard.
- Port: 5173
- Depends on Dashboard Backend


## Usage

Currently the design is that only the `postback-api` on port `8000` and `dash-frontend` on port `5173` would be shared to the world with a proxy like `nginx`. This is how the `demo.openattribution.dev` page is setup, but this seems open for users to customize as they see fit.

 
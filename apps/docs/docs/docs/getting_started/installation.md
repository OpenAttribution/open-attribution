
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

### Services

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


## Deployment in Production

The `postback-api` on port `8000` and `dash-frontend` on port `5173` need to be opened to external internet. This can be done with Nginx reverse proxy. In the below example, this is assuming that the domain is `demo.openattribution.dev`. 

So postbacks would be sent to:
`https://demo.openattribution.dev/collect/impressions/com.myapp&c=...`

And the dashboard would be viewed at:
`https://demo.openattribution.dev/`

The nginx proxy below does not include SSL, as that should be setup with certbot or your own SSL provider. For example, simply running Certbot on the config below will automatically add the correct SSL settings and certificates.

Example `nginx` config, to setup on the same machine, just replace the `server_name` with your domain:
```nginx
server {

  # Replace your domain_name here 
  server_name demo.openattribution.dev;

  add_header Access-Control-Allow-Origin '*';

  # Forward to the dash-frontend
  location / {
    proxy_pass http://localhost:5173;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_hide_header 'Access-Control-Allow-Origin';
  }

  # Forward to the postback-api
   location /collect {
    proxy_pass http://localhost:8000;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_hide_header 'Access-Control-Allow-Origin';
  }
}

```

 
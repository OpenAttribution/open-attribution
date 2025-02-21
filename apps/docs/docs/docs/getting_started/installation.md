!!! warning

    This project is very early stage. I am writing the documentation early to help myself plan where the project should be. That means that many features are not yet built and are a work in progress. If you are interested in the project, please feel free to reach out. For now the project is not appropriate for production ad tracking.

# Docker

While this was originally being built with `bash` and `python` scripts it seems that the more features that were added the less that made sense as a way for different users to deploy. Currently OpenAttribution only supports Docker as a deployment method.

## Step 1: Clone / Copy and Installation

### Clone the repo

The only file you technically need is the `docker-compose.yml` file. But you can get it by cloning the repo:

```sh
git clone https://github.com/openattribution/open-attribution.git
```

### Pull and run ONE of the docker compose files

For development, requires building but many services are have hot reloading for immediate feedback when editing code. Runs random fake data to localhost:8000 which you can see immediately on http://localhost:5173 or in the various services logs. An overview of the services via Dozzle is available at http://localhost:8080.

#### Dev: For developing and contributing to Open Attribution.

```sh
docker compose -f ~/open-attribution/docker/docker-compose-dev.yml pull
docker compose -f ~/open-attribution/docker/docker-compose-dev.yml up -d
```

#### Main: This is for production use. You might wish to copy this file and modify it for your own use away from the repo.

Copy `.production.env-exmaple` to `.production.env` and modify it with your preferred values.

```sh
docker compose -f ~/open-attribution/docker/docker-compose.yml pull
docker compose -f ~/open-attribution/docker/docker-compose.yml up -d
```

If using main, or wanting to secure an instance of Open Attribtuion:

1. Copy `.env-example` to `.env`
2. Modify `.env` with your actual credentials
3. Do not commit `.env` to version control

Docker installs the following services:

### Services

#### Kafka

- Image: `docker.io/bitnami/kafka:3.6.2`
- Ports: 9092 (internal), 9093 (external)

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

## Step 2: Deployment in Production

Check out the Open Attribution SDKs for integration with your preferred platform:

- [iOS SDK](https://github.com/openattribution/oa-ios-sdk)
- [Android SDK](https://github.com/openattribution/oa-android-sdk)
- Let us know which SDKs you are interested in so we can prioritize development!

## Step 3: Expose to the internet

The `postback-api` on port `8000` and `dash-frontend` on port `5173` need to be opened to external internet. This can be done with Nginx reverse proxy. In the below example, this is assuming that the domain is `demo.openattribution.dev`.

So postbacks would be sent to:
`https://demo.openattribution.dev/collect/impressions/com.myapp&c=...`

And the dashboard would be viewed at:
`https://demo.openattribution.dev/`

The nginx proxy below does not include SSL, as that should be setup with certbot or your own SSL provider. For example, simply running Certbot on the config below will automatically add the correct SSL settings and certificates.

Example `nginx` config, to setup on the same machine, just replace the `server_name` with your domain:

Redirects for Postbacks and Dashboard:

```nginx
server {

  # Replace your domain_name here
  server_name demo.openattribution.dev;

  add_header Access-Control-Allow-Origin '*';

  # Forward to the postback-api
  location /collect {
    proxy_pass http://localhost:8000;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_hide_header 'Access-Control-Allow-Origin';
  }

  # Forward to the dash-frontend
  location / {
    proxy_pass http://localhost:5173;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_hide_header 'Access-Control-Allow-Origin';
  }

}

```

Redirects for Share Links, more info in [Share Links](./getting_started/share_links.md)

```nginx
server {
  server_name app.thirdgate.dev;

  listen 80;

  # Forward to postback-api share links endpoint
  location / {
    proxy_pass http://localhost:8000/api/links/share$request_uri;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_hide_header 'Access-Control-Allow-Origin';
  }

}
```

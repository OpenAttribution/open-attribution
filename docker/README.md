# Docker

Note the that databases are frequently changing and are not yet stable.

OpenAttribution dev is `docker-compose-dev.yml` and includes steps for building.

OpenAttribution production is `docker-compose.yml` which uses images from docker repositories.

Usage
```
  Start:          docker compose -f ~/open-attribution/docker/docker-compose-dev.yml up -d
  Down:           docker compose -f ~/open-attribution/docker/docker-compose-dev.yml down
  Stop:           docker compose -f ~/open-attribution/docker/docker-compose-dev.yml stop
  Pull New:       docker compose -f ~/open-attribution/docker/docker-compose-dev.yml pull
  Destroy:        docker compose -f ~/open-attribution/docker/docker-compose-dev.yml down -v --remove-orphans
```

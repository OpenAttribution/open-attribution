
## 

## Launching the demo.openattribution.dev site

Assuming you've cloned Open Attribution to your local home directory `~/open-attribution` you can pull and build the existing docker files:

```
docker compose -f ~/open-attribution/docker/docker-compose-dev.yml pull
docker compose -f ~/open-attribution/docker/docker-compose-dev.yml up -d --build
```

Since developement is quite early, tables and data in the `analytics-db` and `admin-db` regularly need to be dumped and rebuilt. *Do not store anything important there currently*

`docker compose -f ~/open-attribution/docker/docker-compose-dev.yml down -v`


### Writing Docs
This documentation is written in mkdocs and is included in the repository under `apps/docs`.  All doc files should be in markdown. 

Changes in docs can be previewed locally with:

```
pip install mkdocs-material mkdocs-rss-plugin
mkdocs serve
```






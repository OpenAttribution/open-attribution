
# For Developers working on contributing to OpenAttribution

## Launching the demo.openattribution.dev site

Assuming you've cloned Open Attribution to your local home directory `~/open-attribution` you can pull and build the existing docker files:

```sh
docker compose -f ~/open-attribution/docker/docker-compose-dev.yml pull
docker compose -f ~/open-attribution/docker/docker-compose-dev.yml up -d --build
```

Since developement is quite early, tables and data in the `analytics-db` and `admin-db` regularly need to be dumped and rebuilt. *Do not store anything important there currently*

`docker compose -f ~/open-attribution/docker/docker-compose-dev.yml down -v`


## Updating the Documentation Content

All documentation is written in markdown and thus can be edited in any markdown editor. Documentation can be contributed to without servering or running the docs or site unless you want to change menu items or other configurations.

## Serving the Documenation

This documentation is written in the python library`mkdocs` and is included in the repository under `apps/docs`.

Changes in docs can be previewed locally with:

In the a python environment, run:
```sh
pip install mkdocs-material mkdocs-rss-plugin
```

serving the docs happens from the where the mkdocs.yml file is located.

```sh
cd apps/docs/docs/
mkdocs serve
```

and for the blog

```sh
cd apps/docs/blog/
mkdocs serve
```

## Developing the website

The website is built with sveltekit and is located in `apps/www`. Install dependencies with:

```sh
cd apps/www
npm install
```

and run the development server with:

```sh
npm run dev
```






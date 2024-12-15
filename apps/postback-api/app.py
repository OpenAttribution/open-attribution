"""API Endpoints for postbacks to OpenAttribution."""

import logging

from api_app.controllers.postbacks import PostbackController
from api_app.controllers.share import ShareController
from detect.geo import update_geo_dbs
from litestar import Litestar
from litestar.config.cors import CORSConfig
from litestar.logging import LoggingConfig
from litestar.openapi import OpenAPIConfig, OpenAPIController

cors_config = CORSConfig(
    allow_origins=[
        "*",
    ],
)


class MyOpenAPIController(OpenAPIController):
    """Set Docs path."""

    # Should this just move to docs?
    path = "/collect/docs"  # NOTE: not working in prod? works in dev


logging_config = LoggingConfig(
    root={"level": logging.getLevelName(logging.INFO), "handlers": ["console"]},
    formatters={
        "standard": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"},
    },
)

update_geo_dbs()

app = Litestar(
    route_handlers=[PostbackController, ShareController],
    cors_config=cors_config,
    openapi_config=OpenAPIConfig(
        title="Open Attribution Postback API",
        version="0.0.1",
        openapi_controller=MyOpenAPIController,
    ),
    logging_config=logging_config,
    debug=True,
)

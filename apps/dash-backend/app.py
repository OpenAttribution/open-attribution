"""Main start point for LiteStar API."""

import logging

from dash_api.controllers.analytics import OverviewController
from dash_api.controllers.apps import AppController
from dash_api.controllers.links import LinkController
from dash_api.controllers.networks import NetworkController
from litestar import Litestar
from litestar.config.cors import CORSConfig
from litestar.logging import LoggingConfig
from litestar.openapi import OpenAPIConfig, OpenAPIController

cors_config = CORSConfig(
    allow_origins=[
        "localhost",
    ],
)


class MyOpenAPIController(OpenAPIController):
    """Set Path for API docs."""

    path = "/api/docs"


logging_config = LoggingConfig(
    root={"level": logging.getLevelName(logging.INFO), "handlers": ["console"]},
    formatters={
        "standard": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"},
    },
)


app = Litestar(
    route_handlers=[
        OverviewController,
        NetworkController,
        AppController,
        LinkController,
    ],
    cors_config=cors_config,
    openapi_config=OpenAPIConfig(
        title="OpenAttribution Dash Backend API",
        version="0.0.1",
        openapi_controller=MyOpenAPIController,
    ),
    logging_config=logging_config,
    debug=True,
)

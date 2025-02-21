"""Initialize project settings and logging."""

import logging
import os
import pathlib
import sys
from logging.handlers import RotatingFileHandler
from types import TracebackType
from typing import Any

from confluent_kafka import Producer

PROJECT_NAME = "open-attribution"

HOME = pathlib.Path.home()

# load config in /home/my-user/app-store/config.toml
TOP_CONFIGDIR = pathlib.Path(HOME, pathlib.Path(".config"))
CONFIG_DIR = pathlib.Path(TOP_CONFIGDIR, pathlib.Path(PROJECT_NAME))
LOG_DIR = pathlib.Path(CONFIG_DIR, pathlib.Path("logs"))
MODULE_DIR = pathlib.Path(__file__).resolve().parent.parent


def is_docker() -> bool:
    """Decide if we are in docker."""
    path = pathlib.Path("/proc/self/cgroup")
    return pathlib.Path("/.dockerenv").exists() or (
        path.is_file() and any("docker" in line for line in path.open())
    )


KAFKA_LOCATION = "kafka:9092" if is_docker() else "localhost:9092"


def handle_exception(
    # ruff: noqa: ANN401
    exc_type: Any,
    exc_value: BaseException,
    exc_traceback: TracebackType | None,
) -> None:
    """Handle uncaught exceptions."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


def check_config_dirs() -> None:
    """Check that config dirs exist."""
    dirs = [TOP_CONFIGDIR, CONFIG_DIR, LOG_DIR]
    for _dir in dirs:
        if not pathlib.Path.exists(_dir):
            pathlib.Path.mkdir(_dir, exist_ok=True)


def get_logger(mod_name: str, log_name: str = "dash") -> logging.Logger:
    """Create a logger for use in other modules."""
    _format = "%(asctime)s: %(name)s: %(levelname)s: %(message)s"
    check_config_dirs()
    log_dir = pathlib.Path(HOME, pathlib.Path(f".config/{PROJECT_NAME}/logs/testing"))
    if not pathlib.Path.exists(log_dir):
        pathlib.Path.mkdir(log_dir, exist_ok=True)
        # ruff: noqa: T201
        print(f"Couldn't find {log_dir=} so it was created.")
    filename = f"{log_dir}/{log_name}.log"
    # Writes to file
    rotate_handler = RotatingFileHandler(
        filename=filename,
        maxBytes=50000000,
        backupCount=5,
    )
    logging.basicConfig(
        format=_format,
        level=logging.INFO,
        handlers=[
            rotate_handler,
        ],
    )
    # create logger
    logger = logging.getLogger(mod_name)
    logger.setLevel(logging.INFO)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)
    return logger


# Set global handling of uncaught exceptions
sys.excepthook = handle_exception

logger = get_logger(__name__)

DATE_FORMAT = "%Y-%m-%d"

# for non docker local development manually source contents of .dev.env
# ../../docker/.dev.env
# manually like export POSTGRES_USER=postgres
POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_DB = os.environ["POSTGRES_DB"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]


# If inside docker: "bootstrap.servers": "kafka:9092",
reg_config = {
    "bootstrap.servers": KAFKA_LOCATION,
}

event_config = {
    "bootstrap.servers": KAFKA_LOCATION,
    "linger.ms": 1000,  # This is to attempt to slow down events to allow clickhouse mv to process clicks. Should be handled some other way in ClickHouse?
}
IMPRESSION_CLICK_PRODUCER = Producer(reg_config)
EVENT_PRODUCER = Producer(event_config)

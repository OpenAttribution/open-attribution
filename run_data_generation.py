"""Run tests and check results of attributions."""

import argparse

from config import get_logger
from tests.generate_impressions_and_clicks import main as continuously_generate
from tests.test_installs import main as test_installs

logger = get_logger(__name__)


def manage_cli_args() -> argparse.Namespace:
    """Add the CLI arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--installs-test",
        action="store_true",
        help="Generate installs",
        default=False,
    )
    # Argument to accept a list of names
    parser.add_argument(
        "-e",
        "--endpoint-api",
        help="API endpoint for testing",
        default="http://localhost:8000/",
    )
    # Argument to accept a list of names
    parser.add_argument(
        "-n",
        "--names",
        type=lambda s: s.split(","),
        help="List of names separated by commas",
        default=[],
    )
    args = parser.parse_args()
    return args


def main(args: argparse.Namespace) -> None:
    """Run user tests."""
    logger.info(f"Main start with {args=}")
    test_names = args.names
    endpoint = args.endpoint_api
    if endpoint[-1] == "/":
        endpoint = endpoint[:-1]
    if args.installs_test:
        test_installs(endpoint=endpoint, test_names=test_names)
    else:
        continuously_generate(endpoint=endpoint)


if __name__ == "__main__":
    args = manage_cli_args()
    main(args)

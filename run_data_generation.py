"""Run tests and check results of attributions."""

import argparse

from tests.generate_impressions_and_clicks import main as continuously_generate
from tests.test_installs import main as test_installs


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
        "-n",
        "--names",
        type=lambda s: s.split(","),
        help="List of names separated by commas",
        default=[],
    )
    args = parser.parse_args()
    return args


def main(args: argparse.Namespace) -> None:
    """Main entry point for tests."""
    test_names = args.names
    if args.installs_test:
        test_installs(test_names)
    else:
        continuously_generate()


if __name__ == "__main__":
    args = manage_cli_args()
    main(args)

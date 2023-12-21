import argparse

from tests.generate_impressions_and_clicks import main as continuously_generate
from tests.test_installs import main as test_installs


def manage_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--installs-test",
        action="store_true",
        help="Generate installs",
        default=False,
    )
    args = parser.parse_args()
    return args


def main(args: argparse.Namespace) -> None:
    if args.installs_test:
        test_installs()
    else:
        continuously_generate()


if __name__ == "__main__":
    args = manage_cli_args()
    main(args)

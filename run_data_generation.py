import argparse

from tests.generate_impressions_and_clicks import main as continuously_generate
from tests.test_installs import main as generate_simple_321


def manage_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--simple-321",
        action="store_true",
        help="Generate 300 impressions, 200 clicks and 100 installs",
        default=False,
    )
    args, leftovers = parser.parse_known_args()
    return args


def main(args: argparse.Namespace) -> None:
    if args.simple_321:
        generate_simple_321()
    else:
        continuously_generate()


if __name__ == "__main__":
    args = manage_cli_args()
    main(args)

import argparse
from pathlib import Path

from datagen.executor import SingleDatasetExecutor
from models.config import read_config


def parse_args():
    parser = argparse.ArgumentParser("accio")

    parser.add_argument(
        "-f",
        "--file",
        type=Path,
        required=True,
        help="Path to config file",
    )

    parser.add_argument(
        "-s",
        "--seed",
        type=int,
        required=False,
        help="Seed",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    config = read_config(args.file)
    if args.seed:
        config.seed = args.seed
    executor = SingleDatasetExecutor(config)
    executor.run()

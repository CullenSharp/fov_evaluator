"""Does something I swear."""

import argparse
import logging

from fov_evaluator import api
from fov_evaluator.config import GenerateArgs

logger = logging.getLogger(__name__)


def main() -> None:
    """Cli entry point."""
    parser = argparse.ArgumentParser(prog="fov-evaluator")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    logger.info("Running")

    # for testing, run generate with default args
    api.generate(GenerateArgs())

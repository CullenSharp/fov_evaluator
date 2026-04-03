"""Does something I swear."""

import argparse
import logging

from fov_evaluator import api

logger = logging.getLogger(__name__)


def main() -> None:
    """Cli entry point."""
    parser = argparse.ArgumentParser("Evaluates lost for several FOVs")
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    logger.info("Running comprehensive program")

    # for testing, run generate with default args
    api.comprehensive()

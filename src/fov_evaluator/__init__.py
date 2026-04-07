"""Defines the CLI for the project."""

import argparse
import logging
from pathlib import Path

from fov_evaluator import api

logger = logging.getLogger(__name__)


def do_eval(args: argparse.Namespace) -> None:
    """Generate images and run data."""
    if args.all and args.noisey:
        logger.info("Running evaluation for 20, 30, and 45 deg FOV with more noise and motion blur")
        api.comprehensive(noisey=True)
    elif args.all:
        logger.info("Running evaluation for 20, 30, and 45 deg FOV")
        api.comprehensive()
    else:
        logger.error("Invalid argument. Try run eval --help")


def do_clean(args: argparse.Namespace) -> None:
    """Clean out old data."""
    if args.all:
        for fov in [20, 30, 45]:
            logger.info("Cleaning out old data for %d FOV", fov)
            logger.info("Cleaning out old images")
            for img in (Path.cwd() / "imgs" / f"fov{fov}").glob("*.png"):
                img.unlink()

            logger.info("Cleaning out old databases")
            for db in (Path.cwd() / "dbs").glob("*.dat"):
                db.unlink()

            logger.info("Cleaning out old tables")
            for table in (Path.cwd() / "data").glob("*.csv"):
                table.unlink()
    else:
        logger.error("Invalid argument. Try run clean --help")


def main() -> None:
    """Cli entry point."""
    parser = argparse.ArgumentParser("Evaluates lost for several FOVs")
    subparsers = parser.add_subparsers(required=True, help="Clean out data from old runs")
    parser.add_argument("-v", "--verbose", action="store_true")

    clean = subparsers.add_parser("clean", help="Delete data from old runs")
    clean.add_argument("-a", "--all", action="store_true", help="Cleans everything")
    clean.set_defaults(func=do_clean)

    evaluate = subparsers.add_parser("eval", help="Run simulation")
    evaluate.add_argument("-a", "--all", action="store_true")
    evaluate.add_argument("--noisey", action="store_true")
    evaluate.set_defaults(func=do_eval)
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    args.func(args)

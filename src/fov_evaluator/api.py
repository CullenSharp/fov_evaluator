"""Serves as the main entry point for the evaluator."""

import argparse
import logging
import subprocess
from importlib.resources import path

from fov_evaluator.cli_adapter import LostCLIAdapter
from fov_evaluator.config import GenerateArgs

logger = logging.getLogger(__name__)


class LOST:
    """Primary interface for lost."""

    @staticmethod
    def run(args: list[str]) -> subprocess.CompletedProcess:
        """Do work."""
        with path("fov_evaluator.lost", "lost") as cli:
            return subprocess.run(
                args=[str(cli), *args],
                cwd=cli.parent,
                check=True,
                capture_output=True,
            )

    @classmethod
    def generate(cls, cfg: GenerateArgs) -> subprocess.CompletedProcess:
        """Generate synthetic input (imgs) from the lost pipeline."""
        args = LostCLIAdapter.build_args(cfg)
        logger.debug(args)
        return cls.run(args)

    @classmethod
    def comprehensive(cls) -> None:
        """Generate images, db, and estimates."""


def run() -> None:
    """Cli entry point."""
    parser = argparse.ArgumentParser(prog="fov-evaluator")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    logger.info("Running")

    # for testing, run generate with default args
    LOST.generate(GenerateArgs())

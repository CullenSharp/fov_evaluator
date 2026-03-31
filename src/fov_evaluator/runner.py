"""Serves as the main entry point for the evaluator."""

import argparse
import subprocess
from importlib.resources import path
from pathlib import Path
import logging

from fov_evaluator.cli_adapter import LostCLIAdapter
from fov_evaluator.generate import GenerateArgs


class LOST:
    """Primary interface for lost."""

    def run(self, args: list[str]) -> subprocess.CompletedProcess:
        """Do work."""
        with path("fov_evaluator.lost", "lost") as cli:
            return subprocess.run(
                args=[str(cli), *args],
                cwd=cli.parent,
                check=True,
                capture_output=True,
            )

    def generate(self, cfg: GenerateArgs) -> subprocess.CompletedProcess:
        """Generate an image."""
        args = LostCLIAdapter.build_args(cfg)
        logger.debug(args)
        return self.run(args)


def run() -> None:
    """Cli entry point."""
    parser = argparse.ArgumentParser(prog="fov-evaluator")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    gen_args = GenerateArgs()
    lost = LOST()
    lost.generate(gen_args)


logger = logging.getLogger(__name__)

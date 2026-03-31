"""Serves as the main entry point for the evaluator."""

import argparse
import subprocess
from importlib.resources import path

from .generate import GenerateArgs


class LOST:
    """Primary interface for lost."""

    def run(self, args: list[str], *, dry_run: bool = False) -> None | subprocess.CompletedProcess:
        """Do work."""
        result: subprocess.CompletedProcess
        if dry_run:
            print(args)
        else:
            with path("fov_evaluator.lost", "lost") as cli:
                result = subprocess.run(
                    args=[str(cli), *args],
                    cwd=cli.parent,
                    check=True,
                    capture_output=True,
                )
            return result
        return None


def run() -> None:
    """Cli entry point."""
    parser = argparse.ArgumentParser(prog="fov-evaluator")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

"""Serves as the main entry point for the evaluator."""

import argparse
import subprocess
from pathlib import Path


class LOST:
    """Primary interface for lost."""

    cli: Path

    def __init__(self) -> None:
        """Find cli."""
        self.cli = Path(__file__).parents[1] / "lost"

        # check for existence
        if not self.cli.exists():
            raise RuntimeError(f"Can't find {self.cli}.")

    def run(self, args: list, *, dry_run: bool = False) -> None:
        """Do work."""
        if dry_run:
            print(args)
        else:
            subprocess.run(
                args=[str(self.cli), *args], cwd=self.cli.parent, check=True, capture_output=True
            )


def run() -> None:
    """Cli entry point."""
    parser = argparse.ArgumentParser(prog="fov-evaluator")
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()
    print(args.verbose)

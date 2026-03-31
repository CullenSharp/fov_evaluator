"""Serves as the main entry point for the evaluator."""

import argparse
import subprocess
from importlib.resources import path


class LOST:
    """Primary interface for lost."""

    def run(self, args: list, *, dry_run: bool = False) -> None:
        """Do work."""
        if dry_run:
            print(args)
        else:
            with path("fov_evaluator.lost", "lost") as cli:
                subprocess.run(
                    args=[str(cli), *args],
                    cwd=cli.parent,
                    check=True,
                    capture_output=True,
                )


def run() -> None:
    """Cli entry point."""
    parser = argparse.ArgumentParser(prog="fov-evaluator")
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()
    print(args.verbose)

    lost = LOST()
    lost.run(['args'])

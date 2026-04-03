"""Serves as the main entry point for the evaluator."""

import logging
import subprocess
from importlib.resources import path

from fov_evaluator.cli_adapter import LostCLIAdapter
from fov_evaluator.config import GenerateArgs

logger = logging.getLogger(__name__)


def run(args: list[str]) -> subprocess.CompletedProcess:
    """Do work."""
    with path("fov_evaluator.lost", "lost") as cli:
        return subprocess.run(
            args=[str(cli), *args],
            cwd=cli.parent,
            check=True,
            capture_output=True,
        )


def generate(cfg: GenerateArgs) -> subprocess.CompletedProcess:
    """Generate synthetic input (imgs) from the lost pipeline."""
    args = LostCLIAdapter.build_args(cfg)
    logger.debug(args)
    return run(args)


def comprehensive() -> None:
    """Generate images, db, and estimates."""

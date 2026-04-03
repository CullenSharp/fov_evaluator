"""Serves as the main entry point for the evaluator."""

import csv
import logging
import random
import re
import subprocess
from importlib.resources import path
from math import pi
from pathlib import Path

from fov_evaluator.cli_adapter import LostCLIAdapter
from fov_evaluator.config import DatabaseArgs, EstimateArgs, GenerateArgs

logger = logging.getLogger(__name__)

lost_output_re: re.Pattern[str] = re.compile(r"^([a-z0-9_]+) ([a-z0-9.-]+)$")


def run_lost(args: list[str]) -> subprocess.CompletedProcess:
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
    return run_lost(args)


def comprehensive() -> None:
    """Generate images, db, and estimates."""
    synthetic_attitudes: list[tuple[float, float, float]] = []
    fovs: list[int] = [20, 30, 45]

    # generate random attitudes
    with Path("synthetic_attitudes.csv").open("w+", newline="") as spreadsheet:
        attitude_writer = csv.writer(spreadsheet)

        # write table header
        attitude_writer.writerow(["right ascension (deg)", "declination (deg)", "roll (deg)"])
        for _ in range(100):
            ra = round(random.random() * 360, ndigits=2)  # noqa: S311
            de = round(2 * (random.random() - 0.5) * 90, ndigits=2)  # noqa: S311
            roll = round(random.random() * 360, ndigits=2)  # noqa: S311

            synthetic_attitudes.append((ra, de, roll))
            attitude_writer.writerow((ra, de, roll))

    for fov in fovs:
        estimated_attitudes: list[tuple[float, float, float]] = []
        db_path = Path.cwd() / "dbs" / f"fov{fov}.dat"

        # remove all previous images
        logger.info("Running simulation for %d deg FOV", fov)
        logger.info("Removing images from previous run")
        for img in (Path.cwd() / "imgs" / f"fov{fov}").glob("*.png"):
            img.unlink()

        logger.info("Generating database")
        # generate database
        if not db_path.exists():
            db_args = LostCLIAdapter.build_args(DatabaseArgs(output_path=str(db_path)))
            run_lost(db_args)

        logger.info("Generating images and estimates")
        for attitude in synthetic_attitudes:
            ra, de, roll = attitude
            args = LostCLIAdapter.build_args(
                GenerateArgs(fov=fov, ra=ra, de=de, roll=roll)
            ) + LostCLIAdapter.build_args(EstimateArgs(database=str(db_path)))
            lost_output = run_lost(args)

            # extract results
            results: dict[str, float | int] = {}
            for line in lost_output.stdout.decode('ascii').splitlines():
                if matched := lost_output_re.match(line):
                    key = matched.group(1)
                    value_str = matched.group(2)

                    if key == "attitude_known":
                        value: float | int = int(value_str)
                    else:
                        value = float(value_str)

                    results[key] = value

            if results["attitude_known"] == 1:
                estimated_attitudes.append(
                    (
                        results["attitude_ra"],
                        results["attitude_de"],
                        results["attitude_roll"],
                    )
                )
            else:
                # if miss id'd write bogus results
                estimated_attitudes.append((9999.0, 9999.0, 9999.0))

        logger.info("Writing results to tables")
        with Path(f"fov{fov}_estimated_attitudes.csv").open("w+", newline="") as spreadsheet:
            attitude_writer = csv.writer(spreadsheet)

            # write table header
            attitude_writer.writerow(["right ascension (deg)", "declination (deg)", "roll (deg)"])
            for attitude in estimated_attitudes:
                attitude_writer.writerow(attitude)

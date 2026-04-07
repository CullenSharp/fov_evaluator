"""Serves as the main entry point for the evaluator."""

import csv
import logging
import random
import re
import subprocess
from collections.abc import Iterable
from importlib.resources import path
from pathlib import Path

from fov_evaluator.cli_adapter import LostCLIAdapter
from fov_evaluator.config import DatabaseArgs, EstimateArgs, GenerateArgs

logger = logging.getLogger(__name__)

lost_output_re: re.Pattern[str] = re.compile(r"^([a-z0-9_]+) ([a-z0-9.-]+)$")


def progress_bar(
    iteration: int,
    total: int,
    decimals: int = 1,
    length: int = 100,
) -> str:
    """Return a progress_bar."""
    fill: str = "█"
    percent = f"{100 * (iteration / float(total)):.{decimals}f}"
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + "-" * (length - filled_length)
    return f"|{bar}| {percent}%"


def attitudes_to_csv(name: str, attitudes: Iterable) -> None:
    """Write data to a csv given a path."""
    with (Path.cwd() / "data" / f"{name}.csv").open("w+", newline="") as spreadsheet:
        attitude_writer = csv.writer(spreadsheet)
        attitude_writer.writerow(["right ascension (deg)", "declination (deg)", "roll (deg)"])
        for attitude in attitudes:
            attitude_writer.writerow(attitude)


def synthesize_attitudes(n: int = 100) -> list[tuple[float, float, float]]:
    """Create n random attitudes.

    ra in [0, 360] deg
    de in [-90, 90] deg
    roll in [0, 360] deg
    """
    synthetic_attitudes: list[tuple[float, float, float]] = []
    for _ in range(n):
        ra = round(random.random() * 360, ndigits=6)  # noqa: S311
        de = round(2 * (random.random() - 0.5) * 90, ndigits=6)  # noqa: S311
        roll = round(random.random() * 360, ndigits=6)  # noqa: S311

        synthetic_attitudes.append((ra, de, roll))

    return synthetic_attitudes


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


def comprehensive(*, noisey: bool = False) -> None:
    """Generate images, db, and estimates."""
    fovs: list[int] = [20, 30, 45]

    # generate random attitudes
    synthetic_attitudes: list[tuple[float, float, float]] = synthesize_attitudes(n=100)
    attitudes_to_csv(name="synthetic_attitudes", attitudes=synthetic_attitudes)

    for fov in fovs:
        estimated_attitudes: list[tuple[float, float, float]] = []
        db_path = Path.cwd() / "dbs" / f"fov{fov}.dat"

        # remove all previous images
        logger.info("Running evaluation for %d deg FOV", fov)
        logger.info("Removing images from previous run")
        for img in (Path.cwd() / "imgs" / f"fov{fov}").glob("*.png"):
            img.unlink()

        logger.info("Generating database")
        # generate database
        if not db_path.exists():
            db_args = LostCLIAdapter.build_args(
                DatabaseArgs(kvector_max_distance=fov, output_path=str(db_path))
            )
            run_lost(db_args)

        logger.info("Generating images and estimates")
        for iteration, attitude in enumerate(synthetic_attitudes):
            ra, de, roll = attitude
            if not noisey:
                args = LostCLIAdapter.build_args(
                    GenerateArgs(fov=fov, ra=ra, de=de, roll=roll)
                ) + LostCLIAdapter.build_args(EstimateArgs(database=str(db_path)))
            else:
                args = LostCLIAdapter.build_args(
                    GenerateArgs(
                        dark_current=0.25,
                        de=de,
                        de_motion_blur=0,
                        read_noise=0.05,
                        exposure=0.2,
                        false_stars=400,
                        fov=fov,
                        ra=ra,
                        ra_motion_blur=0.3,
                        roll=roll,
                        roll_motion_blur=4,
                        saturation_photons=25,
                        zero_mag_photons=10_000,
                    )
                ) + LostCLIAdapter.build_args(
                    EstimateArgs(brightest_filter=12, database=str(db_path), mag_filter=5)
                )
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
                # if miss write bogus results
                estimated_attitudes.append((9999.0, 9999.0, 9999.0))

            # show progress
            print(
                f"\rProgress {progress_bar(iteration=iteration + 1, total=100)}",
                flush=True,
                end="\r",
            )

        print("\n")
        logger.info("Writing results to tables")
        attitudes_to_csv(name=f"fov{fov}_estimated_attitudes", attitudes=estimated_attitudes)

    logger.info("Done!")

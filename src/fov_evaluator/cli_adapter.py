"""Serves as the translation layer to the LOST cli."""

import logging
from dataclasses import asdict
from pathlib import Path
from typing import ClassVar, overload

from fov_evaluator.config import DatabaseArgs, EstimateArgs, GenerateArgs

logger = logging.getLogger(__name__)


class LostCLIAdapter:
    """Translation layer to lost cli."""

    arg_map: ClassVar[dict[str, str]] = {
        # input generator args
        "dark_current": "--generate-dark-current",
        "de": "--generate-de",
        "de_motion_blur": "--generate-blur-de",
        "exposure": "--generate-exposure",
        "false_stars": "--generate-false-stars",
        "fov": "--fov",
        "ra": "--generate-ra",
        "ra_motion_blur": "--generate-blur-ra",
        "read_noise": "--generate-read-noise",
        "roll": "--generate-roll",
        "roll_motion_blur": "--generate-blur-roll",
        "saturation_photons": "--generate-saturation-photons",
        "x_res": "--generate-x-resolution",
        "y_res": "--generate-y-resolution",
        "zero_mag_photons": "--generate-zero-mag-photons",
        # database args
        "kvector_max_distance": "--kvector-max-distance",
        # estimation args
        "angular_tolerance": "--angular-tolerance",
        "attitude_algo": "--attitude-algo",
        "centroid_algo": "--centroid-algo",
        "database": "--database",
        "mag_filter": "--centroid-mag-filter",
        "min_mag": "--min-mag",
        "output_path": "--output",
        "star_id_algo": "--star-id-algo",
        "brightest_filter": "--centroid-filter-brightest",
    }

    @overload
    @classmethod
    def build_args(cls, cfg: EstimateArgs) -> list[str]:
        pass

    @overload
    @classmethod
    def build_args(cls, cfg: GenerateArgs) -> list[str]:
        pass

    @overload
    @classmethod
    def build_args(cls, cfg: DatabaseArgs) -> list[str]:
        pass

    @classmethod
    def build_args(cls, cfg: EstimateArgs | GenerateArgs | DatabaseArgs) -> list[str]:
        """Build argument list."""
        # assume that the input is for the pipeline subcommand
        args: list[str] = []

        # inputs to pipeline subcommand
        if isinstance(cfg, EstimateArgs):
            for arg, value in asdict(cfg).items():
                args.append(cls.arg_map[arg])
                args.append(str(value))
            args.append("--print-attitude=-")
        if isinstance(cfg, GenerateArgs):
            args.append("pipeline")
            args.append("--generate=1")
            for arg, value in asdict(cfg).items():
                args.append(cls.arg_map[arg])
                args.append(str(value))
            args.append("--plot-raw-input")

            # append file name
            args.append(f"{Path.cwd() / 'imgs' / f'fov{cfg.fov}' / cfg.fname}")

        if isinstance(cfg, DatabaseArgs):
            # redirect arguments to the database subcommand
            args.append("database")
            args.append("--kvector")
            for arg, value in asdict(cfg).items():
                args.append(cls.arg_map[arg])
                args.append(str(value))

        return args

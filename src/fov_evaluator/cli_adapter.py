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
        "false_stars": "--generate-false-stars",
        "zero_mag_photons": "--generate-zero-mag-photons",
        "saturation_photons": "--generate-saturation-photons",
        "dark_current": "--generate-dark-current",
        "exposure": "--generate-exposure",
        "read_noise": "--generate-read-noise",
        "x_res": "--generate-x-resolution",
        "y_res": "--generate-y-resolution",
        "fov": "--fov",
        "ra": "--generate-ra",
        "de": "--generate-de",
        "roll": "--generate-roll",
        "kvector_max_distance": "--kvector-max-distance",
        "min_mag": "--min-mag",
        "centroid_algo": "--centroid-algo",
        "star_id_algo": "--star-id-algo",
        "attitude_algo": "--attitude-algo",
        "output_path": "--output",
        "database": "--database",
        "angular_tolerance": "--angular-tolerance",
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
            args.append(f"{Path.cwd() / 'imgs' / f'fov{cfg.fov}' / cfg.get_fname()}")

        if isinstance(cfg, DatabaseArgs):
            # redirect arguments to the database subcommand
            args.append("database")
            args.append("--kvector")
            for arg, value in asdict(cfg).items():
                args.append(cls.arg_map[arg])
                args.append(str(value))

        return args

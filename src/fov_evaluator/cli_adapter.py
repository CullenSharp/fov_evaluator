"""Serves as the translation layer to the LOST cli."""

from dataclasses import asdict
from pathlib import Path
from typing import ClassVar, overload

from fov_evaluator.config import DatabaseArgs, EstimateArgs, GenerateArgs


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
        args: list[str] = ["pipeline"]

        # inputs to pipeline subcommand
        if isinstance(cfg, EstimateArgs):
            for arg, value in asdict(cfg).items():
                args.append(cls.arg_map[arg])
                args.append(str(value))
        if isinstance(cfg, GenerateArgs):
            args = ["--generate", "1"]
            for arg, value in asdict(cfg).items():
                args.append(cls.arg_map[arg])
                args.append(str(value))
            args.append("--plot-raw-input")

            # append file name
            args.append(f"{Path.cwd() / 'imgs' / f'fov{cfg.fov}' / cfg.get_name()}")

        if isinstance(cfg, DatabaseArgs):
            # redirect arguments to the database subcommand
            args[0] = "database"
            for arg, value in asdict(cfg).items():
                args.append(cls.arg_map[arg])
                args.append(str(value))
        return args

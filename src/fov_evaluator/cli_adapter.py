"""Serves as the translation layer to the LOST cli."""

from dataclasses import asdict
from pathlib import Path
from typing import ClassVar

from .generate import GenerateArgs


class LostCLIAdapter:
    """Translation layer to lost cli."""

    arg_map: ClassVar[dict] = {
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

    @classmethod
    def build_args(cls, cfg: GenerateArgs) -> list[str]:
        """Build argument list."""
        args = ["pipeline", "--generate", "1"]
        for arg, value in asdict(cfg).items():
            args.append(cls.arg_map[arg])
            args.append(str(value))
        args.append("--plot-raw-input")

        # append file name
        args.append(f"{Path.cwd() / 'imgs' / f'fov{cfg.fov}' / cfg.get_name()}")

        return args

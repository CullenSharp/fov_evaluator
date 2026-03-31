"""Helper classes for generating images."""

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class GenerateArgs:
    """A conveinance object for working with command line arguments."""

    false_stars: int = 50
    zero_mag_photons: int = 20_000
    saturation_photons: int = 50
    dark_current: float = 0.25
    exposure: float = 0.2
    read_noise: float = 0.02

    # orientation params
    fov: int = 30  # angular field of view
    ra: int = 88  # right ascenion
    de: int = 0  # declination
    roll: int = 7

    # image size
    x_res: int = 1024
    y_res: int = 1024

    def get_name(self) -> str:
        """Construct name."""
        name = f"fov{self.fov}ra{self.ra}roll{self.roll}de{self.de}.png"
        logger.debug(name)
        return name

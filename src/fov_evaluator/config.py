"""Helper classes for generating images."""

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class GenerateArgs:
    """Configuration object for generating synthetic input.

    orientation params
    declination: [-90 deg, 90 deg] --> [-pi/2 rad, pi/2 rad]
                where negative means south
                of the celestial equator and positive means north
    right ascenion: [0 deg, 360 deg] --> [0 rad, 2pi rad ]
    roll: [0 rad, 2 pi rad]ms
    """

    false_stars: int = 50
    zero_mag_photons: int = 20_000
    saturation_photons: int = 50
    dark_current: float = 0.25
    exposure: float = 0.2
    read_noise: float = 0.02
    fov: int = 30

    # orientation params
    ra: int = 88
    de: int = 0
    roll: int = 7

    # image size
    x_res: int = 1024
    y_res: int = 1024

    def get_name(self) -> str:
        """Construct name."""
        name = f"fov{self.fov}ra{self.ra}roll{self.roll}de{self.de}.png"
        logger.debug(name)
        return name


@dataclass
class DatabaseArgs:
    """Configuration object for generating databases."""


@dataclass
class EstimateArgs:
    """Configuration object for generating estimates."""

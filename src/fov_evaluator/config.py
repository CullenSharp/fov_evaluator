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
    fov: int = 20

    # orientation params
    ra: float = 88.0
    de: float = 0.0
    roll: float = 7.0

    # image size
    x_res: int = 1024
    y_res: int = 1024

    def get_fname(self) -> str:
        """Construct file name."""
        name = f"fov{self.fov}ra{int(self.ra)}roll{int(self.roll)}de{int(self.de)}.png"
        logger.debug("Generated filename %s:", name)
        return name


@dataclass
class DatabaseArgs:
    """Configuration object for generating databases."""

    output_path: str = ""
    kvector_max_distance: int = 25
    min_mag: float = 5.0


@dataclass
class EstimateArgs:
    """Configuration object for generating estimates."""

    centroid_algo: str = "cog"
    star_id_algo: str = "py"
    attitude_algo: str = "dqm"
    angular_tolerance: float = 0.03
    database: str = ""

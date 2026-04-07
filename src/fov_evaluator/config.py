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

    dark_current: float = 0.25
    de_motion_blur: float = 0
    exposure: float = 0.2
    false_stars: int = 50
    fov: int = 20
    ra_motion_blur: float = 0
    read_noise: float = 0.02
    roll_motion_blur: float = 0
    saturation_photons: int = 50
    zero_mag_photons: int = 20_000

    # orientation params
    de: float = 0.0
    ra: float = 88.0
    roll: float = 7.0

    # image size
    x_res: int = 1024
    y_res: int = 1024

    @property
    def fname(self) -> str:
        """Construct a file name for the synthetic input."""
        return f"fov{self.fov}ra{int(self.ra)}roll{int(self.roll)}de{int(self.de)}.png"


@dataclass
class DatabaseArgs:
    """Configuration object for generating databases."""

    output_path: str = ""
    kvector_max_distance: int = 25
    min_mag: float = 5.0


@dataclass
class EstimateArgs:
    """Configuration object for generating estimates."""

    angular_tolerance: float = 0.03
    attitude_algo: str = "dqm"
    brightest_filter: int = 8
    centroid_algo: str = "cog"
    database: str = ""
    mag_filter: int = 5
    star_id_algo: str = "py"

"""Helper classes for generating images."""

from dataclasses import asdict, dataclass


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
        return f"fov{self.fov}ra{self.ra}roll{self.roll}de{self.de}.png"

    def to_args(self) -> list:
        """Generate a list of arguments from the class fields."""
        arg_map = {
            "false_stars": "--generate-false-stars",
            "zero_mag_photons": "--generate-zero-mag-photons",
            "saturation_photons": "--generate-saturation-photons",
            "dark_current": "--generate-dark-current",
            "x_res": "--generate-x-resolution",
            "y_res": "--generate-y-resolution",
            "fov": "--fov",
            "ra": "--generate-ra",
            "de": "--generate-de",
            "roll": "--generate-roll",
        }

        # flatten the class
        args = ["pipeline", "--generate", "1"]
        for arg, value in asdict(self).items():
            args.append(arg_map[arg])
            args.append(str(value))
        args.append("--plot-raw-input")

        # append file name
        args.append(self.get_name())

        return args

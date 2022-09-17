"""A package for loading XDF files recorded with TMSi amplifiers.

This package exposes the following functions:

- `read_raw_xdf(
    xdf_fname: PathLike,
    stream_picks: int | str = 1,
    scale: int | float = 1e-6,
    verbose: VerbosityLevel = True,
)` - Reader for .xdf files recorded with TMSi amplifiers.

"""

__version__ = "0.1.0.dev1"

from .xdf import read_raw_xdf

"""Travel carbon utilities for Taiwan HEI Scope 3 Category 6 workflows.

Pure functions extracted for testability and JOSS packaging. The Tkinter GUI
in the repository root remains the primary end-user entry point.
"""

from .carbon import (
    CARBON_EMISSION_FACTORS,
    calculate_carbon_emission,
    determine_transport_mode,
)
from .geo_text import normalize_place_text, strip_admin_suffix
from .zoom import calculate_zoom_level

__all__ = [
    "CARBON_EMISSION_FACTORS",
    "determine_transport_mode",
    "calculate_carbon_emission",
    "calculate_zoom_level",
    "normalize_place_text",
    "strip_admin_suffix",
]

__version__ = "0.1.0"

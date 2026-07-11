"""Travel carbon utilities for Taiwan HEI Scope 3 Category 6 workflows.

Pure functions extracted for testability and JOSS packaging. The Tkinter GUI
in the repository root remains the primary end-user entry point.
"""

from .carbon import (
    CARBON_EMISSION_FACTORS,
    calculate_carbon_emission,
    determine_transport_mode,
    get_emission_factors,
    reload_emission_factors,
    sensitivity_compare,
)
from .pipeline import estimate_trip
from .eval_batch import evaluate_gold_csv
from .maps_meta import route_map_meta
from .data import (
    ALIASES,
    CHINA_KEYWORDS,
    COORDINATES,
    INTERNATIONAL_CITY_MAPPING,
    TAIWAN_REGION_MAPPING,
)
from .geo_text import normalize_place_text, strip_admin_suffix
from .distance import (
    compute_driving_distance,
    compute_flight_distance,
    compute_island_flight_distance,
    geodesic_km,
    get_osrm_route,
)
from .locations import (
    classify_trip_kind,
    is_domestic,
    resolve_coordinates,
    smart_destination_handler,
)
from .zoom import calculate_zoom_level

__all__ = [
    "CARBON_EMISSION_FACTORS",
    "determine_transport_mode",
    "calculate_carbon_emission",
    "calculate_zoom_level",
    "normalize_place_text",
    "strip_admin_suffix",
    "COORDINATES",
    "ALIASES",
    "TAIWAN_REGION_MAPPING",
    "INTERNATIONAL_CITY_MAPPING",
    "CHINA_KEYWORDS",
    "smart_destination_handler",
    "is_domestic",
    "resolve_coordinates",
    "classify_trip_kind",
    "geodesic_km",
    "get_osrm_route",
    "compute_driving_distance",
    "compute_island_flight_distance",
    "compute_flight_distance",
    "get_emission_factors",
    "reload_emission_factors",
    "sensitivity_compare",
    "estimate_trip",
    "evaluate_gold_csv",
    "route_map_meta",
]

__version__ = "0.1.0"

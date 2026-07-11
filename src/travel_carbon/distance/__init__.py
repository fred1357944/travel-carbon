"""Distance engines: geodesic (offline) and optional OSRM (network)."""

from .compute import (
    compute_driving_distance,
    compute_flight_distance,
    compute_island_flight_distance,
    normalize_driving_destination,
    normalize_flight_destination,
)
from .geodesic import geodesic_km, geodesic_km_rounded
from .osrm import get_osrm_route

__all__ = [
    "geodesic_km",
    "geodesic_km_rounded",
    "get_osrm_route",
    "compute_driving_distance",
    "compute_island_flight_distance",
    "compute_flight_distance",
    "normalize_driving_destination",
    "normalize_flight_destination",
]

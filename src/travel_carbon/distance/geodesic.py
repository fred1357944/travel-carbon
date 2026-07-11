"""Geodesic distance helpers (offline)."""

from __future__ import annotations

from typing import Tuple

from geopy.distance import geodesic as _geodesic

# When OSRM is unavailable, approximate road distance ≈ geodesic × factor
DEFAULT_ROAD_FACTOR = 1.4
# Rough duration: minutes per road-km (GUI heuristic)
DEFAULT_MIN_PER_ROAD_KM = 1.5
# Cruise speed assumptions for flight-time heuristics
ISLAND_FLIGHT_KMH = 500.0
INTL_FLIGHT_KMH = 800.0
FLIGHT_FIXED_HOURS = 0.5  # taxi/climb/descent allowance


def geodesic_km(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    road_factor: float = 1.0,
) -> float:
    """Great-circle kilometres between two WGS84 points.

    ``road_factor`` multiplies the geodesic (e.g. 1.4 for crude road estimate).
    """
    km = _geodesic((lat1, lon1), (lat2, lon2)).kilometers
    return float(km) * float(road_factor)


def geodesic_km_rounded(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    road_factor: float = 1.0,
    ndigits: int = 1,
) -> float:
    return round(geodesic_km(lat1, lon1, lat2, lon2, road_factor=road_factor), ndigits)


def estimate_road_duration_min(distance_km: float, min_per_km: float = DEFAULT_MIN_PER_ROAD_KM) -> int:
    return int(round(float(distance_km) * float(min_per_km)))


def estimate_flight_hours(distance_km: float, cruise_kmh: float, fixed_hours: float = FLIGHT_FIXED_HOURS) -> float:
    if cruise_kmh <= 0:
        return fixed_hours
    return float(distance_km) / float(cruise_kmh) + float(fixed_hours)


def latlon_pair(entry: dict) -> Tuple[float, float]:
    return (float(entry["lat"]), float(entry["lon"]))

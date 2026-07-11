"""End-to-end offline-friendly trip estimation helpers."""

from __future__ import annotations

from typing import Any, Dict, MutableMapping, Optional

from travel_carbon.carbon import calculate_carbon_emission, get_emission_factors
from travel_carbon.distance import (
    compute_driving_distance,
    compute_flight_distance,
    compute_island_flight_distance,
)
from travel_carbon.locations import classify_trip_kind, smart_destination_handler


def estimate_trip(
    destination: str,
    *,
    row: Optional[dict] = None,
    kind: Optional[str] = None,
    use_osrm: bool = False,
    route_cache: Optional[MutableMapping[str, dict]] = None,
    factor_profile: str = "screening",
) -> Dict[str, Any]:
    """Resolve destination → distance → carbon for one free-text place.

    Parameters
    ----------
    kind:
        Optional force: ``mainland`` | ``island`` | ``international``.
        Default: ``classify_trip_kind``.
    use_osrm:
        Only for mainland driving; default False for offline demos/tests.
    factor_profile:
        ``screening`` or ``taiwan_cfp`` (see carbon.get_emission_factors).
    """
    row = row or {}
    raw = "" if destination is None else str(destination).strip()
    handled = smart_destination_handler(raw) if raw else ""
    trip_kind = kind or classify_trip_kind(raw)

    cache = route_cache if route_cache is not None else {}
    if trip_kind == "unknown" or not raw:
        dist = {
            "序號": row.get("序號"),
            "傳票編號": row.get("傳票編號"),
            "目的地": raw or "(empty)",
            "類型": "未知",
            "距離(km)": 0,
            "時間": "N/A",
            "起點": None,
            "終點": {"name": raw or "(empty)", "lat": 0, "lon": 0},
            "route": None,
            "route_key": "unknown-empty",
            "cached": False,
        }
    elif trip_kind == "island":
        dist = compute_island_flight_distance(handled or raw, row=row, route_cache=cache)
    elif trip_kind == "international":
        dist = compute_flight_distance(handled or raw, row=row, route_cache=cache)
    else:
        dist = compute_driving_distance(
            handled or raw,
            row=row,
            route_cache=cache,
            use_osrm=use_osrm,
        )

    factors = get_emission_factors(factor_profile)
    carbon = calculate_carbon_emission(
        str(dist.get("類型") or ""),
        float(dist.get("距離(km)") or 0),
        factors=factors,
    )
    return {
        "input": destination,
        "normalized": handled,
        "kind": trip_kind,
        "distance": dist,
        "carbon": carbon,
        "factor_profile": factor_profile,
    }

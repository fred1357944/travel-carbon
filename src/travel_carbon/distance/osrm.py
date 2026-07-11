"""OSRM driving-route client (network optional)."""

from __future__ import annotations

from typing import Any, Dict, Optional

DEFAULT_OSRM_URL = "http://router.project-osrm.org/route/v1/driving"


def get_osrm_route(
    start_lat: float,
    start_lon: float,
    end_lat: float,
    end_lon: float,
    *,
    base_url: str = DEFAULT_OSRM_URL,
    timeout: float = 10.0,
) -> Optional[Dict[str, Any]]:
    """Query OSRM for a driving route.

    Returns dict with distance_km, duration_min, geometry — or None on failure.
    """
    try:
        import requests
    except ImportError:
        return None

    try:
        url = f"{base_url}/{start_lon},{start_lat};{end_lon},{end_lat}"
        params = {"overview": "full", "geometries": "geojson"}
        response = requests.get(url, params=params, timeout=timeout)
        if response.status_code != 200:
            return None
        data = response.json()
        if data.get("code") != "Ok" or not data.get("routes"):
            return None
        route = data["routes"][0]
        return {
            "distance_km": round(route["distance"] / 1000, 1),
            "duration_min": round(route["duration"] / 60),
            "geometry": route.get("geometry"),
            "raw": route,
        }
    except Exception:
        return None

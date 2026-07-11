"""Lightweight map metadata (no Folium dependency for unit tests)."""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

from travel_carbon.zoom import calculate_zoom_level


def route_map_meta(result: Dict[str, Any]) -> Dict[str, Any]:
    """Derive center / zoom for a distance result dict (audit-map prep)."""
    start = result.get("起點") or {}
    end = result.get("終點") or {}
    try:
        slat = float(start.get("lat") or 0)
        slon = float(start.get("lon") or 0)
        elat = float(end.get("lat") or 0)
        elon = float(end.get("lon") or 0)
    except (TypeError, ValueError):
        slat = slon = elat = elon = 0.0

    if slat == 0 and elat == 0:
        center = (25.03, 121.5)
        zoom = 7
    else:
        center = ((slat + elat) / 2.0, (slon + elon) / 2.0)
        zoom = calculate_zoom_level(float(result.get("距離(km)") or 0))

    return {
        "center_lat": center[0],
        "center_lon": center[1],
        "zoom": zoom,
        "has_geometry": result.get("route") is not None,
        "start_name": start.get("name"),
        "end_name": end.get("name"),
        "distance_km": result.get("距離(km)"),
        "trip_type": result.get("類型"),
    }


def bounds_from_result(result: Dict[str, Any]) -> Optional[Tuple[Tuple[float, float], Tuple[float, float]]]:
    """Return ((min_lat, min_lon), (max_lat, max_lon)) or None."""
    start = result.get("起點") or {}
    end = result.get("終點") or {}
    try:
        points = [
            (float(start["lat"]), float(start["lon"])),
            (float(end["lat"]), float(end["lon"])),
        ]
    except (KeyError, TypeError, ValueError):
        return None
    if any(abs(a) < 1e-9 and abs(b) < 1e-9 for a, b in points):
        # incomplete coords
        if all(abs(a) < 1e-9 and abs(b) < 1e-9 for a, b in points):
            return None
    lats = [p[0] for p in points]
    lons = [p[1] for p in points]
    return ((min(lats), min(lons)), (max(lats), max(lons)))

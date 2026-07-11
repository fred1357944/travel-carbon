"""Trip distance builders for mainland drive / island air / international air."""

from __future__ import annotations

from typing import Any, Dict, MutableMapping, Optional

from travel_carbon.data import (
    CHINA_KEYWORDS,
    COORDINATES,
    INTERNATIONAL_CITY_MAPPING,
    TAIWAN_REGION_MAPPING,
)
from travel_carbon.distance.geodesic import (
    DEFAULT_ROAD_FACTOR,
    INTL_FLIGHT_KMH,
    ISLAND_FLIGHT_KMH,
    estimate_flight_hours,
    estimate_road_duration_min,
    geodesic_km_rounded,
    latlon_pair,
)
from travel_carbon.distance.osrm import get_osrm_route

ORIGIN_CAMPUS = "輔仁大學"
ORIGIN_TSA = "松山機場"
ORIGIN_TPE = "桃園機場"


def _empty_row(row: Optional[dict] = None) -> Dict[str, Any]:
    row = row or {}
    return {
        "序號": row.get("序號"),
        "傳票編號": row.get("傳票編號"),
    }


def _lookup_coord_key(name: str) -> Optional[str]:
    if not name:
        return None
    if name in COORDINATES:
        return name
    alt = name.replace("臺", "台")
    if alt in COORDINATES:
        return alt
    alt2 = name.replace("台", "臺")
    if alt2 in COORDINATES:
        return alt2
    return None


def normalize_driving_destination(destination: str) -> str:
    """Map district labels to city keys used for driving OD."""
    if destination in TAIWAN_REGION_MAPPING:
        return TAIWAN_REGION_MAPPING[destination]
    key = _lookup_coord_key(destination)
    return key or destination


def normalize_flight_destination(destination: str) -> str:
    """Map secondary cities to airport/country keys for international legs."""
    if destination in INTERNATIONAL_CITY_MAPPING:
        return INTERNATIONAL_CITY_MAPPING[destination]
    # China free-text: find first known city → hub
    for china_city, airport in INTERNATIONAL_CITY_MAPPING.items():
        if china_city in destination:
            return airport
    for city in CHINA_KEYWORDS:
        if city in destination and city in INTERNATIONAL_CITY_MAPPING:
            return INTERNATIONAL_CITY_MAPPING[city]
        if city in destination and _lookup_coord_key(city):
            return _lookup_coord_key(city)  # type: ignore[return-value]
    key = _lookup_coord_key(destination)
    return key or destination


def compute_driving_distance(
    destination: str,
    *,
    row: Optional[dict] = None,
    origin_key: str = ORIGIN_CAMPUS,
    route_cache: Optional[MutableMapping[str, dict]] = None,
    use_osrm: bool = True,
    road_factor: float = DEFAULT_ROAD_FACTOR,
) -> Dict[str, Any]:
    """Campus → destination road distance (OSRM preferred, geodesic×factor fallback)."""
    row = row or {}
    original = destination
    if destination in INTERNATIONAL_CITY_MAPPING:
        # Wrong mode — callers should use flight; keep soft fail as zero unknown
        return {
            **_empty_row(row),
            "目的地": original,
            "類型": "未知",
            "距離(km)": 0,
            "時間": "N/A",
            "起點": dict(COORDINATES.get(origin_key, {"name": origin_key, "lat": 0, "lon": 0})),
            "終點": {"name": original, "lat": 0, "lon": 0},
            "route": None,
            "route_key": f"unknown-{original}",
            "cached": False,
        }

    dest_key = normalize_driving_destination(destination)
    dest_key = _lookup_coord_key(dest_key) or dest_key

    if dest_key not in COORDINATES:
        # try decompose original
        for region, parent in TAIWAN_REGION_MAPPING.items():
            if region in original:
                dest_key = _lookup_coord_key(parent) or parent
                break

    origin = COORDINATES.get(origin_key)
    if not origin or dest_key not in COORDINATES:
        return {
            **_empty_row(row),
            "目的地": original,
            "類型": "未知",
            "距離(km)": 0,
            "時間": "N/A",
            "起點": dict(origin or {"name": origin_key, "lat": 0, "lon": 0}),
            "終點": {"name": original, "lat": 0, "lon": 0},
            "route": None,
            "route_key": f"unknown-{original}",
            "cached": False,
        }

    end = COORDINATES[dest_key]
    route_key = f"{origin_key}-{dest_key}-driving"
    cache = route_cache if route_cache is not None else {}

    if route_key in cache:
        c = cache[route_key]
        return {
            **_empty_row(row),
            "目的地": f"{original} ({c['終點']['name']})",
            "類型": c["類型"],
            "距離(km)": c["距離(km)"],
            "時間": c["時間"],
            "起點": c["起點"],
            "終點": c["終點"],
            "route": c.get("route"),
            "route_key": route_key,
            "cached": True,
        }

    route_geom = None
    if use_osrm:
        osrm = get_osrm_route(origin["lat"], origin["lon"], end["lat"], end["lon"])
        if osrm:
            distance_km = osrm["distance_km"]
            duration_min = osrm["duration_min"]
            route_geom = osrm.get("geometry")
            payload = {
                "目的地": f"{original} ({end['name']})",
                "類型": "國內-開車",
                "距離(km)": distance_km,
                "時間": f"{duration_min}分鐘",
                "起點": origin,
                "終點": end,
                "route": route_geom,
            }
            cache[route_key] = payload
            return {
                **_empty_row(row),
                **payload,
                "route_key": route_key,
                "cached": False,
            }

    # Fallback: geodesic × road factor
    distance_km = geodesic_km_rounded(
        origin["lat"], origin["lon"], end["lat"], end["lon"], road_factor=road_factor
    )
    duration_min = estimate_road_duration_min(distance_km)
    payload = {
        "目的地": f"{original} ({end['name']})",
        "類型": "國內-開車",
        "距離(km)": distance_km,
        "時間": f"{duration_min}分鐘",
        "起點": origin,
        "終點": end,
        "route": None,
    }
    cache[route_key] = payload
    return {
        **_empty_row(row),
        **payload,
        "route_key": route_key,
        "cached": False,
    }


def compute_island_flight_distance(
    destination: str,
    *,
    row: Optional[dict] = None,
    route_cache: Optional[MutableMapping[str, dict]] = None,
) -> Dict[str, Any]:
    """Songshan (default) → offshore island geodesic flight."""
    row = row or {}
    original = destination
    dest_key = _lookup_coord_key(destination) or destination
    if dest_key not in COORDINATES:
        return {
            **_empty_row(row),
            "目的地": original,
            "類型": "離島-未知",
            "距離(km)": 0,
            "時間": "N/A",
            "起點": dict(COORDINATES.get(ORIGIN_TSA, {"name": ORIGIN_TSA, "lat": 25.0694, "lon": 121.5526})),
            "終點": {"name": original, "lat": 0, "lon": 0},
            "route": None,
            "route_key": f"unknown-{original}",
            "cached": False,
        }

    if dest_key in ("澎湖", "金門", "馬祖") or COORDINATES[dest_key].get("type") == "island":
        start = COORDINATES[ORIGIN_TSA]
        flight_type = "國內-離島航班"
    else:
        start = COORDINATES[ORIGIN_TPE]
        flight_type = "國內-航班"

    end = COORDINATES[dest_key]
    route_key = f"{start['name']}-{dest_key}-island-flight"
    cache = route_cache if route_cache is not None else {}

    if route_key in cache:
        c = cache[route_key]
        return {
            **_empty_row(row),
            "目的地": f"{original} ({c['終點']['name']})",
            "類型": c["類型"],
            "距離(km)": c["距離(km)"],
            "時間": c["時間"],
            "起點": c["起點"],
            "終點": c["終點"],
            "route": None,
            "route_key": route_key,
            "cached": True,
        }

    la, lo = latlon_pair(start)
    lb, lob = latlon_pair(end)
    distance_km = geodesic_km_rounded(la, lo, lb, lob, road_factor=1.0)
    hours = estimate_flight_hours(distance_km, ISLAND_FLIGHT_KMH)
    payload = {
        "目的地": f"{dest_key} ({end['name']})",
        "類型": flight_type,
        "距離(km)": distance_km,
        "時間": f"{hours:.1f}小時",
        "起點": start,
        "終點": end,
    }
    cache[route_key] = payload
    return {
        **_empty_row(row),
        "目的地": f"{original} ({end['name']})",
        "類型": flight_type,
        "距離(km)": distance_km,
        "時間": f"{hours:.1f}小時",
        "起點": start,
        "終點": end,
        "route": None,
        "route_key": route_key,
        "cached": False,
    }


def compute_flight_distance(
    destination: str,
    *,
    row: Optional[dict] = None,
    route_cache: Optional[MutableMapping[str, dict]] = None,
) -> Dict[str, Any]:
    """Taoyuan → international hub geodesic flight."""
    row = row or {}
    original = destination

    if destination in TAIWAN_REGION_MAPPING:
        # wrong mode — return driving instead via compute_driving
        return compute_driving_distance(
            destination, row=row, route_cache=route_cache, use_osrm=False
        )

    dest_key = normalize_flight_destination(destination)
    dest_key = _lookup_coord_key(dest_key) or dest_key

    if dest_key not in COORDINATES:
        return {
            **_empty_row(row),
            "目的地": original,
            "類型": "國際-未知",
            "距離(km)": 0,
            "時間": "N/A",
            "起點": dict(COORDINATES.get(ORIGIN_TPE, {"name": ORIGIN_TPE, "lat": 25.0777, "lon": 121.2325})),
            "終點": {"name": original, "lat": 0, "lon": 0},
            "route": None,
            "route_key": f"unknown-{original}",
            "cached": False,
        }

    start = COORDINATES[ORIGIN_TPE]
    end = COORDINATES[dest_key]
    route_key = f"{ORIGIN_TPE}-{dest_key}-flying"
    cache = route_cache if route_cache is not None else {}

    if route_key in cache:
        c = cache[route_key]
        return {
            **_empty_row(row),
            "目的地": f"{original} ({c['終點']['name']})",
            "類型": c["類型"],
            "距離(km)": c["距離(km)"],
            "時間": c["時間"],
            "起點": c["起點"],
            "終點": c["終點"],
            "route": None,
            "route_key": route_key,
            "cached": True,
        }

    la, lo = latlon_pair(start)
    lb, lob = latlon_pair(end)
    distance_km = geodesic_km_rounded(la, lo, lb, lob, road_factor=1.0)
    hours = estimate_flight_hours(distance_km, INTL_FLIGHT_KMH)
    payload = {
        "目的地": f"{dest_key} ({end['name']})",
        "類型": "國際-飛行",
        "距離(km)": distance_km,
        "時間": f"{hours:.1f}小時",
        "起點": start,
        "終點": end,
    }
    cache[route_key] = payload
    return {
        **_empty_row(row),
        "目的地": f"{original} ({end['name']})",
        "類型": "國際-飛行",
        "距離(km)": distance_km,
        "時間": f"{hours:.1f}小時",
        "起點": start,
        "終點": end,
        "route": None,
        "route_key": route_key,
        "cached": False,
    }

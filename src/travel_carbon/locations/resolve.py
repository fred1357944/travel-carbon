"""Resolve free-text destinations against the built-in gazetteer."""

from __future__ import annotations

from typing import Any, Dict, Optional

from travel_carbon.data import (
    ALIASES,
    CHINA_KEYWORDS,
    COORDINATES,
    INTERNATIONAL_CITY_MAPPING,
    TAIWAN_REGION_MAPPING,
)
from travel_carbon.geo_text import normalize_place_text, strip_admin_suffix

# Taiwan mainland city keys (drive from campus); islands use flight path
TAIWAN_MAINLAND_CITIES = [
    "台北",
    "臺北",
    "新北",
    "桃園",
    "新竹",
    "苗栗",
    "台中",
    "臺中",
    "彰化",
    "南投",
    "雲林",
    "嘉義",
    "台南",
    "臺南",
    "高雄",
    "屏東",
    "宜蘭",
    "花蓮",
    "台東",
    "臺東",
    "基隆",
]
TAIWAN_ISLANDS = ["澎湖", "金門", "馬祖"]

CHINA_PROVINCES = [
    "浙江",
    "江蘇",
    "廣東",
    "福建",
    "山東",
    "河北",
    "河南",
    "湖北",
    "湖南",
    "四川",
    "陕西",
    "山西",
    "遼寧",
    "吉林",
    "黑龍江",
    "安徽",
    "江西",
    "雲南",
    "貴州",
    "甘肅",
    "青海",
]


def smart_destination_handler(destination: str) -> str:
    """Normalize a destination string for downstream coordinate lookup.

    Mirrors the GUI ``_smart_destination_handler`` logic:
    aliases → strip suffixes → district-in-city → China province+city → international map.
    """
    if not destination:
        return ""
    original = str(destination).strip()
    destination = original

    # Alias table (case-insensitive for Latin keys)
    lower = destination.lower()
    if lower in ALIASES:
        destination = ALIASES[lower]
    elif destination in ALIASES:
        destination = ALIASES[destination]

    # Remove common trailing administrative suffixes one layer
    for suffix in ("市", "縣", "區", "鎮", "鄉", "街", "路", "段"):
        if destination.endswith(suffix):
            destination = destination[: -len(suffix)]
            break

    # e.g. "台北市南港區" style: both region and parent appear → prefer region
    for region, parent in TAIWAN_REGION_MAPPING.items():
        if region in destination and parent in destination:
            return region
        # also check original for full compound strings
        if region in original and parent in original:
            return region

    # China: province + city in original text → city
    for province in CHINA_PROVINCES:
        if province in original:
            for city in CHINA_KEYWORDS:
                if city in original:
                    return city

    if destination in INTERNATIONAL_CITY_MAPPING:
        return destination

    return destination


def is_domestic(destination: str) -> bool:
    """True for Taiwan mainland destinations (drive); False for islands/abroad.

    Island destinations return False so the GUI can route them as domestic air.
    """
    if not destination:
        return False
    destination = str(destination)

    if any(island in destination for island in TAIWAN_ISLANDS):
        return False

    taiwan_regions = list(TAIWAN_REGION_MAPPING.keys())
    is_taiwan_mainland = any(city in destination for city in TAIWAN_MAINLAND_CITIES) or any(
        region in destination for region in taiwan_regions
    )

    if any(city in destination for city in CHINA_KEYWORDS):
        return False

    # Direct coordinate type lookup after light normalization
    key = destination
    if key not in COORDINATES:
        key = destination.replace("臺", "台")
    if key not in COORDINATES:
        key = destination.replace("台", "臺")
    if key in COORDINATES:
        t = COORDINATES[key].get("type")
        if t == "domestic":
            return True
        if t == "island":
            return False
        if t == "international":
            return False
        if t == "airport":
            # airports may be domestic hubs; treat as non-mainland drive default
            return key in ("松山機場",) or "台灣" in COORDINATES[key].get("name", "")

    return is_taiwan_mainland


def resolve_coordinates(name: str) -> Optional[Dict[str, Any]]:
    """Map a free-text place to a COORDINATES entry, or None."""
    if not name:
        return None
    raw = str(name).strip()
    handled = smart_destination_handler(raw)

    candidates = []
    for cand in (
        handled,
        raw,
        normalize_place_text(handled),
        strip_admin_suffix(handled),
        handled.replace("臺", "台"),
        handled.replace("台", "臺"),
        normalize_place_text(raw),
    ):
        if cand and cand not in candidates:
            candidates.append(cand)

    # District → parent city for coordinate lookup when district missing as drive target
    if handled in TAIWAN_REGION_MAPPING:
        parent = TAIWAN_REGION_MAPPING[handled]
        if parent not in candidates:
            candidates.append(parent)

    # International city may map to country/airport hub key
    if handled in INTERNATIONAL_CITY_MAPPING:
        hub = INTERNATIONAL_CITY_MAPPING[handled]
        if hub not in candidates:
            candidates.append(hub)
        # also try city itself if in COORDINATES
        if handled not in candidates:
            candidates.append(handled)

    for cand in candidates:
        if cand in COORDINATES:
            return dict(COORDINATES[cand])
        # alias may produce key present in COORDINATES
        mapped = ALIASES.get(cand) or ALIASES.get(cand.lower() if cand else "")
        if mapped and mapped in COORDINATES:
            return dict(COORDINATES[mapped])

    return None


def classify_trip_kind(destination: str) -> str:
    """High-level trip class for routing policy labels."""
    if not destination or not str(destination).strip():
        return "unknown"
    d = smart_destination_handler(destination)
    if not d:
        return "unknown"
    if any(island in d or island in destination for island in TAIWAN_ISLANDS):
        return "island"
    if is_domestic(d) or is_domestic(destination):
        return "mainland"
    if d in INTERNATIONAL_CITY_MAPPING or any(c in destination for c in CHINA_KEYWORDS):
        return "international"
    info = resolve_coordinates(d)
    if info:
        t = info.get("type")
        if t == "island":
            return "island"
        if t == "domestic" or t == "start":
            return "mainland"
        if t in ("international", "airport"):
            # airport alone is ambiguous; international hubs → international
            if t == "airport" and info.get("name", "").find("國際") >= 0:
                return "international"
            if t == "international":
                return "international"
    # Unresolved free text must NOT silently become international (0 km / 0 kg).
    return "unknown"

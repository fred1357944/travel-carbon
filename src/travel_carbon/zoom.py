"""Map zoom heuristics for Folium audit maps."""

from __future__ import annotations


def calculate_zoom_level(distance_km: float) -> int:
    """Return a Leaflet zoom level appropriate for the trip distance.

    Bands match the desktop tool / ``map_utils`` convention so route maps
    remain readable from intra-city to intercontinental scales.
    """
    if distance_km is None or distance_km < 0:
        return 6
    if distance_km < 10:
        return 13
    if distance_km < 20:
        return 12
    if distance_km < 40:
        return 11
    if distance_km < 80:
        return 10
    if distance_km < 150:
        return 9
    if distance_km < 300:
        return 8
    if distance_km < 600:
        return 7
    if distance_km < 1500:
        return 6
    if distance_km < 3000:
        return 5
    if distance_km < 6000:
        return 4
    return 3

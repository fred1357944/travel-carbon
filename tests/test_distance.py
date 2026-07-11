"""Offline distance tests (no OSRM network)."""

import pytest

from travel_carbon.data import COORDINATES
from travel_carbon.distance import (
    compute_driving_distance,
    compute_flight_distance,
    compute_island_flight_distance,
    geodesic_km,
    geodesic_km_rounded,
)


def test_geodesic_fju_taipei_band():
    a = COORDINATES["輔仁大學"]
    b = COORDINATES["台北"]
    km = geodesic_km(a["lat"], a["lon"], b["lat"], b["lon"])
    assert 10.0 < km < 25.0


def test_road_factor_increases_distance():
    a = COORDINATES["輔仁大學"]
    b = COORDINATES["台中"]
    g = geodesic_km(a["lat"], a["lon"], b["lat"], b["lon"], road_factor=1.0)
    r = geodesic_km(a["lat"], a["lon"], b["lat"], b["lon"], road_factor=1.4)
    assert r == pytest.approx(g * 1.4)


def test_driving_offline_fallback():
    cache = {}
    r = compute_driving_distance("台北", route_cache=cache, use_osrm=False)
    assert r["類型"] == "國內-開車"
    assert r["距離(km)"] > 10
    assert r["cached"] is False
    assert "輔仁大學-台北-driving" in r["route_key"]
    # second call hits cache
    r2 = compute_driving_distance("台北", route_cache=cache, use_osrm=False)
    assert r2["cached"] is True


def test_driving_district_maps_to_city():
    r = compute_driving_distance("南港", use_osrm=False)
    assert r["類型"] == "國內-開車"
    assert r["距離(km)"] > 0
    assert r["終點"]["name"]  # resolved


def test_island_flight_kinmen():
    r = compute_island_flight_distance("金門")
    assert r["類型"] == "國內-離島航班"
    assert r["起點"]["name"] in ("台北松山機場", "松山機場") or "松山" in r["起點"]["name"]
    assert 200 < r["距離(km)"] < 500


def test_international_japan():
    r = compute_flight_distance("日本")
    assert r["類型"] == "國際-飛行"
    assert r["距離(km)"] > 1500
    assert "桃園" in r["起點"]["name"] or r["起點"].get("name")


def test_suzhou_maps_to_shanghai_hub():
    r = compute_flight_distance("蘇州")
    assert r["類型"] == "國際-飛行"
    assert r["距離(km)"] > 500
    # hub should be Shanghai coords
    assert r["終點"]["lat"] == COORDINATES["上海"]["lat"]


def test_unknown_destination_zero():
    r = compute_driving_distance("完全不存在的地方XYZ", use_osrm=False)
    assert r["距離(km)"] == 0
    assert r["類型"] == "未知"


def test_geodesic_rounded():
    a = COORDINATES["輔仁大學"]
    b = COORDINATES["高雄"]
    v = geodesic_km_rounded(a["lat"], a["lon"], b["lat"], b["lon"], ndigits=1)
    assert isinstance(v, float)
    assert v > 200

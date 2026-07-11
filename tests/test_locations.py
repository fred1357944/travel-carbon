"""Offline tests for gazetteer resolution (no network)."""

from travel_carbon.data import COORDINATES, INTERNATIONAL_CITY_MAPPING, TAIWAN_REGION_MAPPING
from travel_carbon.locations import (
    classify_trip_kind,
    is_domestic,
    resolve_coordinates,
    smart_destination_handler,
)


def test_coordinates_core_keys():
    assert "輔仁大學" in COORDINATES
    assert COORDINATES["輔仁大學"]["lat"] == 25.0356
    assert COORDINATES["台北"]["type"] == "domestic"
    assert COORDINATES["金門"]["type"] == "island"
    assert COORDINATES["日本"]["type"] == "international"


def test_district_mapping():
    assert TAIWAN_REGION_MAPPING["南港"] == "台北"
    assert TAIWAN_REGION_MAPPING["板橋"] == "新北"


def test_smart_alias_taipei():
    assert smart_destination_handler("taipei") == "台北"
    assert smart_destination_handler("台北市") in ("台北", "臺北")


def test_smart_compound_nangang():
    # district preferred when both parent and district present
    assert smart_destination_handler("台北市南港區") == "南港"


def test_smart_china_province_city():
    out = smart_destination_handler("浙江省杭州市")
    assert out == "杭州"


def test_is_domestic_mainland_vs_island():
    assert is_domestic("台北") is True
    assert is_domestic("南港") is True
    assert is_domestic("高雄") is True
    assert is_domestic("金門") is False
    assert is_domestic("澎湖") is False


def test_is_domestic_china_and_japan():
    assert is_domestic("上海") is False
    assert is_domestic("日本") is False


def test_resolve_coordinates_basic():
    fju = resolve_coordinates("輔仁大學")
    assert fju is not None
    assert fju["lat"] == 25.0356
    tpe = resolve_coordinates("台北市")
    assert tpe is not None
    assert tpe["type"] == "domestic"


def test_resolve_district_via_mapping():
    # 南港 may resolve to its own coords or parent path
    info = resolve_coordinates("南港")
    assert info is not None
    assert info.get("type") in ("domestic",)


def test_resolve_suzhou_hub():
    assert INTERNATIONAL_CITY_MAPPING["蘇州"] == "上海"
    # may resolve to 蘇州 if present else hub 上海
    info = resolve_coordinates("蘇州")
    assert info is not None


def test_classify_trip_kind():
    assert classify_trip_kind("台中") == "mainland"
    assert classify_trip_kind("金門") == "island"
    assert classify_trip_kind("東京") == "international"


def test_zhongli_maps_to_taoyuan_mainland():
    assert TAIWAN_REGION_MAPPING["中壢"] == "桃園"
    assert is_domestic("中壢") is True
    assert classify_trip_kind("中壢") == "mainland"
    assert resolve_coordinates("中壢") is not None

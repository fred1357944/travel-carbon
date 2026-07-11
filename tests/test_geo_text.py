from travel_carbon.geo_text import normalize_place_text, strip_admin_suffix


def test_normalize_tai_variant():
    assert normalize_place_text("臺北市") == "台北市"
    assert normalize_place_text("台北") == "台北"


def test_normalize_empty():
    assert normalize_place_text(None) == ""
    assert normalize_place_text("  ") == ""


def test_strip_admin_suffix():
    assert strip_admin_suffix("台北市") == "台北"
    assert strip_admin_suffix("新北市板橋區") in ("新北板橋", "新北市板橋", "板橋")
    # full strip of trailing layers
    assert strip_admin_suffix("高雄市") == "高雄"


def test_strip_idempotent_on_city_name():
    assert strip_admin_suffix("東京") == "東京"

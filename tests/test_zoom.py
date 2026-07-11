from travel_carbon.zoom import calculate_zoom_level


def test_local_zoom():
    assert calculate_zoom_level(5) == 13


def test_metro_zoom():
    assert calculate_zoom_level(30) == 11


def test_intercity_zoom():
    assert calculate_zoom_level(200) == 8


def test_intercontinental_zoom():
    assert calculate_zoom_level(9000) == 3

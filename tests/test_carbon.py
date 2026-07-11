"""Unit tests for distance-based carbon helpers."""

from travel_carbon.carbon import (
    CARBON_EMISSION_FACTORS,
    calculate_carbon_emission,
    determine_transport_mode,
)


def test_international_flight_mode():
    mode, factor = determine_transport_mode("國際-飛行", 2000)
    assert mode == "國際航班"
    assert factor == CARBON_EMISSION_FACTORS["國際航班"]


def test_island_flight_mode():
    mode, factor = determine_transport_mode("國內-離島航班", 300)
    assert mode == "國內航班"
    assert factor == CARBON_EMISSION_FACTORS["國內航班"]


def test_driving_short_is_car():
    mode, _ = determine_transport_mode("國內-開車", 50)
    assert mode == "自用車/計程車"


def test_driving_long_assumes_hsr():
    mode, factor = determine_transport_mode("國內-開車", 350)
    assert mode == "火車/高鐵"
    assert factor == CARBON_EMISSION_FACTORS["火車/高鐵"]


def test_zero_distance():
    mode, factor = determine_transport_mode("國內-開車", 0)
    assert mode == "N/A"
    assert factor == 0


def test_emission_calculation():
    out = calculate_carbon_emission("國際-飛行", 1000)
    assert out["交通方式"] == "國際航班"
    assert out["碳排係數"] == 0.101
    assert out["碳排放量(kg CO2e)"] == 101.0


def test_emission_zero_distance():
    out = calculate_carbon_emission("國內-開車", 0)
    assert out["碳排放量(kg CO2e)"] == 0.0

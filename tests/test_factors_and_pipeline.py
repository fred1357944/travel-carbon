"""Tests for factors.yaml loading and estimate_trip pipeline."""

from pathlib import Path

from travel_carbon.carbon import (
    CARBON_EMISSION_FACTORS,
    get_emission_factors,
    load_factors_yaml,
    sensitivity_compare,
)
from travel_carbon.pipeline import estimate_trip


def test_load_factors_yaml_has_screening():
    doc = load_factors_yaml()
    assert doc, "factors.yaml should be discoverable"
    factors = get_emission_factors("screening")
    assert factors["火車/高鐵"] == 0.034
    assert factors["自用車/計程車"] == 0.21


def test_taiwan_cfp_profile_lowers_car_factor():
    screening = get_emission_factors("screening")
    cfp = get_emission_factors("taiwan_cfp")
    assert cfp["自用車/計程車"] == 0.115
    assert cfp["火車/高鐵"] == 0.034
    # car screening higher than CFP private car
    assert screening["自用車/計程車"] > cfp["自用車/計程車"]


def test_module_defaults_match_screening():
    assert CARBON_EMISSION_FACTORS["國際航班"] == 0.101


def test_sensitivity_compare_keys():
    out = sensitivity_compare("國內-開車", 100)
    assert "screening" in out and "taiwan_cfp" in out
    assert out["screening"]["碳排放量(kg CO2e)"] == 21.0
    assert out["taiwan_cfp"]["碳排放量(kg CO2e)"] == 11.5


def test_estimate_trip_taichung_offline():
    r = estimate_trip("台中", use_osrm=False)
    assert r["kind"] == "mainland"
    assert r["distance"]["距離(km)"] > 100
    assert r["carbon"]["碳排放量(kg CO2e)"] > 0


def test_estimate_trip_japan():
    r = estimate_trip("日本", use_osrm=False)
    assert r["kind"] == "international"
    assert r["distance"]["類型"] == "國際-飛行"
    assert r["carbon"]["交通方式"] == "國際航班"


def test_estimate_trip_kinmen():
    r = estimate_trip("金門")
    assert r["kind"] == "island"
    assert "離島" in r["distance"]["類型"] or "航班" in r["distance"]["類型"]


def test_package_factors_file_exists():
    p = Path(__file__).resolve().parents[1] / "src" / "travel_carbon" / "data" / "factors.yaml"
    assert p.is_file()

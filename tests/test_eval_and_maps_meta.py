from pathlib import Path

from travel_carbon.eval_batch import evaluate_gold_csv, write_report
from travel_carbon.maps_meta import bounds_from_result, route_map_meta
from travel_carbon.pipeline import estimate_trip


def test_empty_destination_unknown():
    r = estimate_trip("")
    assert r["kind"] == "unknown"
    assert r["distance"]["距離(km)"] == 0


def test_gold_eval_perfect_on_sample():
    gold = Path(__file__).resolve().parents[1] / "examples" / "sample_travel_gold.csv"
    report = evaluate_gold_csv(gold, use_osrm=False)
    assert report.n == 10
    assert report.kind_accuracy == 1.0
    assert report.mode_accuracy == 1.0
    assert report.total_distance_km > 0
    assert report.total_emission_kg_taiwan_cfp > 0
    # CFP car lower → often lower or equal total vs screening for domestic-heavy set
    assert report.total_emission_kg_taiwan_cfp <= report.total_emission_kg_screening * 1.05


def test_write_report(tmp_path):
    gold = Path(__file__).resolve().parents[1] / "examples" / "sample_travel_gold.csv"
    report = evaluate_gold_csv(gold)
    write_report(report, tmp_path / "report.json", tmp_path / "report.md")
    assert (tmp_path / "report.json").is_file()
    assert "kind accuracy" in (tmp_path / "report.md").read_text(encoding="utf-8")


def test_route_map_meta():
    r = estimate_trip("高雄", use_osrm=False)
    meta = route_map_meta(r["distance"])
    assert meta["zoom"] >= 3
    assert meta["center_lat"] != 0
    b = bounds_from_result(r["distance"])
    assert b is not None

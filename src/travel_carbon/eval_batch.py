"""Offline batch evaluation against a small gold CSV (no network required)."""

from __future__ import annotations

import csv
import json
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from travel_carbon.pipeline import estimate_trip


@dataclass
class RowEval:
    序號: str
    目的地: str
    expected_kind: str
    predicted_kind: str
    kind_ok: bool
    distance_km: float
    trip_type: str
    mode: str
    emission_kg: float
    mode_ok: Optional[bool] = None
    notes: str = ""


@dataclass
class BatchReport:
    n: int = 0
    kind_correct: int = 0
    kind_accuracy: float = 0.0
    mode_checked: int = 0
    mode_correct: int = 0
    mode_accuracy: float = 0.0
    total_distance_km: float = 0.0
    total_emission_kg_screening: float = 0.0
    total_emission_kg_taiwan_cfp: float = 0.0
    by_kind: Dict[str, int] = field(default_factory=dict)
    rows: List[Dict[str, Any]] = field(default_factory=list)
    failures: List[Dict[str, Any]] = field(default_factory=list)


def _read_gold(path: Path) -> List[dict]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def evaluate_gold_csv(
    gold_path: Path,
    *,
    use_osrm: bool = False,
) -> BatchReport:
    """Score kind classification (+ optional mode substring) on a gold file."""
    rows_in = _read_gold(gold_path)
    report = BatchReport()
    kind_counts: Counter = Counter()
    eval_rows: List[RowEval] = []

    for raw in rows_in:
        dest = (raw.get("目的地") or "").strip()
        expected = (raw.get("expected_kind") or "").strip()
        mode_sub = (raw.get("expected_mode_contains") or "").strip()
        r_screen = estimate_trip(dest, use_osrm=use_osrm, factor_profile="screening")
        r_cfp = estimate_trip(dest, use_osrm=use_osrm, factor_profile="taiwan_cfp")

        pred = r_screen["kind"]
        kind_ok = pred == expected if expected else True
        dist = r_screen["distance"]
        carbon = r_screen["carbon"]
        mode = str(carbon.get("交通方式") or "")
        mode_ok: Optional[bool] = None
        if mode_sub:
            mode_ok = mode_sub in mode or mode_sub in str(dist.get("類型") or "")
            report.mode_checked += 1
            if mode_ok:
                report.mode_correct += 1

        report.n += 1
        if kind_ok:
            report.kind_correct += 1
        kind_counts[pred] += 1
        report.total_distance_km += float(dist.get("距離(km)") or 0)
        report.total_emission_kg_screening += float(carbon.get("碳排放量(kg CO2e)") or 0)
        report.total_emission_kg_taiwan_cfp += float(
            r_cfp["carbon"].get("碳排放量(kg CO2e)") or 0
        )

        row_eval = RowEval(
            序號=str(raw.get("序號") or ""),
            目的地=dest,
            expected_kind=expected,
            predicted_kind=pred,
            kind_ok=kind_ok,
            distance_km=float(dist.get("距離(km)") or 0),
            trip_type=str(dist.get("類型") or ""),
            mode=mode,
            emission_kg=float(carbon.get("碳排放量(kg CO2e)") or 0),
            mode_ok=mode_ok,
            notes=str(raw.get("notes") or ""),
        )
        eval_rows.append(row_eval)
        if not kind_ok or mode_ok is False:
            report.failures.append(asdict(row_eval))

    report.kind_accuracy = report.kind_correct / report.n if report.n else 0.0
    report.mode_accuracy = (
        report.mode_correct / report.mode_checked if report.mode_checked else 0.0
    )
    report.by_kind = dict(kind_counts)
    report.rows = [asdict(r) for r in eval_rows]
    # round totals
    report.total_distance_km = round(report.total_distance_km, 1)
    report.total_emission_kg_screening = round(report.total_emission_kg_screening, 3)
    report.total_emission_kg_taiwan_cfp = round(report.total_emission_kg_taiwan_cfp, 3)
    report.kind_accuracy = round(report.kind_accuracy, 4)
    report.mode_accuracy = round(report.mode_accuracy, 4)
    return report


def write_report(report: BatchReport, out_json: Path, out_md: Optional[Path] = None) -> None:
    out_json.parent.mkdir(parents=True, exist_ok=True)
    payload = asdict(report)
    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    if out_md:
        lines = [
            "# Offline eval report",
            "",
            f"- n = **{report.n}**",
            f"- kind accuracy = **{report.kind_accuracy}** ({report.kind_correct}/{report.n})",
            f"- mode accuracy = **{report.mode_accuracy}** ({report.mode_correct}/{report.mode_checked})",
            f"- total distance (screening path) = **{report.total_distance_km}** km",
            f"- total CO₂e screening = **{report.total_emission_kg_screening}** kg",
            f"- total CO₂e taiwan_cfp = **{report.total_emission_kg_taiwan_cfp}** kg",
            "",
            "## By predicted kind",
            "",
        ]
        for k, v in sorted(report.by_kind.items()):
            lines.append(f"- {k}: {v}")
        if report.failures:
            lines += ["", "## Failures", ""]
            for f in report.failures:
                lines.append(
                    f"- #{f['序號']} `{f['目的地']}` expected={f['expected_kind']} "
                    f"got={f['predicted_kind']} mode={f['mode']}"
                )
        else:
            lines += ["", "## Failures", "", "_None_", ""]
        out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def default_gold_path() -> Path:
    # repo examples/
    return Path(__file__).resolve().parents[2] / "examples" / "sample_travel_gold.csv"


def main(argv: Optional[List[str]] = None) -> int:
    import argparse

    p = argparse.ArgumentParser(description="Offline gold CSV evaluation")
    p.add_argument(
        "--gold",
        type=Path,
        default=None,
        help="gold CSV path (default: examples/sample_travel_gold.csv)",
    )
    p.add_argument(
        "--out-dir",
        type=Path,
        default=Path("outputs/eval"),
        help="output directory for report.json / report.md",
    )
    p.add_argument("--osrm", action="store_true")
    args = p.parse_args(argv)

    gold = args.gold or default_gold_path()
    if not gold.is_file():
        # try cwd-relative
        alt = Path("examples/sample_travel_gold.csv")
        gold = alt if alt.is_file() else gold
    if not gold.is_file():
        print(f"gold file not found: {gold}")
        return 1

    report = evaluate_gold_csv(gold, use_osrm=args.osrm)
    write_report(report, args.out_dir / "report.json", args.out_dir / "report.md")
    print(f"kind_accuracy={report.kind_accuracy} mode_accuracy={report.mode_accuracy}")
    print(f"wrote {args.out_dir / 'report.json'}")
    print(f"wrote {args.out_dir / 'report.md'}")
    return 0 if report.kind_accuracy == 1.0 else 2


if __name__ == "__main__":
    raise SystemExit(main())

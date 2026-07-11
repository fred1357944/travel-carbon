"""Distance-based GHG factors and mode heuristics for business travel.

Aligned with GHG Protocol Scope 3 Category 6 (distance-based method).
Default factors load from ``factors.yaml`` when available; see
``docs/emission_factors_notes.md`` for honesty notes vs Taiwan MOENV tables.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Mapping, MutableMapping, Optional, Tuple

# Built-in fallbacks if YAML missing (kg CO2e / km screening defaults)
_BUILTIN_FACTORS: Dict[str, float] = {
    "自用車/計程車": 0.21,
    "國內航班": 0.133,
    "國際航班": 0.101,
    "火車/高鐵": 0.034,
    "巴士": 0.065,
}

HSR_DISTANCE_KM = 300
DOMESTIC_FLIGHT_DISTANCE_KM = 500

# Map GUI mode labels → optional recommended CFP keys (sensitivity set)
_CFP_MODE_ALIASES: Dict[str, Tuple[str, ...]] = {
    "自用車/計程車": ("營業小客車_汽油", "自用小客車_汽油"),
    "火車/高鐵": ("高速鐵路運輸服務",),
    "巴士": ("自用大客車_柴油", "營業大客車_市區公路客運_柴油"),
    # aviation: only route-specific CFP available; leave screening unless forced
}


def _factors_yaml_candidates() -> list[Path]:
    here = Path(__file__).resolve().parent
    return [
        here / "data" / "factors.yaml",
        here.parents[1] / "data" / "factors.yaml",  # src/../data when nested oddly
        here.parents[2] / "data" / "factors.yaml",  # repo root data/
    ]


def load_factors_yaml(path: Optional[Path] = None) -> Dict[str, object]:
    """Load full factors document (dict). Empty dict if unavailable."""
    try:
        import yaml  # type: ignore
    except ImportError:
        yaml = None

    paths = [path] if path else _factors_yaml_candidates()
    for p in paths:
        if p is None or not Path(p).is_file():
            continue
        text = Path(p).read_text(encoding="utf-8")
        if yaml is not None:
            data = yaml.safe_load(text) or {}
            if isinstance(data, dict):
                data["_loaded_from"] = str(Path(p).resolve())
                return data
        # Minimal parser for project_screening_defaults only (no PyYAML)
        return _parse_screening_fallback(text, Path(p))
    return {}


def _parse_screening_fallback(text: str, path: Path) -> Dict[str, object]:
    """Tiny YAML subset reader for project_screening_defaults.*.factor."""
    factors: Dict[str, float] = {}
    in_block = False
    current_mode: Optional[str] = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if line.startswith("project_screening_defaults:"):
            in_block = True
            continue
        if in_block:
            if line and not line.startswith(" ") and not line.startswith("\t") and line.endswith(":"):
                # next top-level key
                if line != "project_screening_defaults:":
                    break
            if line.startswith("  ") and not line.startswith("    ") and line.strip().endswith(":"):
                current_mode = line.strip()[:-1]
            elif current_mode and "factor:" in line:
                try:
                    factors[current_mode] = float(line.split("factor:")[-1].strip())
                except ValueError:
                    pass
    return {
        "project_screening_defaults": {
            k: {"factor": v} for k, v in factors.items()
        },
        "_loaded_from": str(path.resolve()),
        "_parser": "fallback",
    }


def screening_factors_from_doc(doc: Mapping[str, object]) -> Dict[str, float]:
    raw = doc.get("project_screening_defaults") or {}
    out: Dict[str, float] = {}
    if isinstance(raw, dict):
        for mode, meta in raw.items():
            if isinstance(meta, dict) and "factor" in meta:
                out[str(mode)] = float(meta["factor"])
            elif isinstance(meta, (int, float)):
                out[str(mode)] = float(meta)
    return out


def recommended_cfp_from_doc(doc: Mapping[str, object]) -> Dict[str, float]:
    raw = doc.get("recommended_taiwan_cfp_pkm") or {}
    out: Dict[str, float] = {}
    if isinstance(raw, dict):
        for mode, meta in raw.items():
            if isinstance(meta, dict) and "factor" in meta:
                out[str(mode)] = float(meta["factor"])
            elif isinstance(meta, (int, float)):
                out[str(mode)] = float(meta)
    return out


def get_emission_factors(
    profile: str = "screening",
    *,
    factors_path: Optional[Path] = None,
    overrides: Optional[Mapping[str, float]] = None,
) -> Dict[str, float]:
    """Return mode → kg CO2e/km (or pkm) factor dict.

    Profiles
    --------
    screening
        GUI defaults (possibly from YAML).
    taiwan_cfp
        Recommended CFP pkm set mapped onto GUI mode labels where possible;
        unmapped modes keep screening values.
    """
    doc = load_factors_yaml(factors_path)
    screening = screening_factors_from_doc(doc) or dict(_BUILTIN_FACTORS)
    # ensure all builtin keys exist
    for k, v in _BUILTIN_FACTORS.items():
        screening.setdefault(k, v)

    if profile == "screening":
        factors = dict(screening)
    elif profile == "taiwan_cfp":
        cfp = recommended_cfp_from_doc(doc)
        factors = dict(screening)
        # map known modes
        if "自用小客車_汽油" in cfp:
            factors["自用車/計程車"] = cfp["自用小客車_汽油"]
        if "營業小客車_汽油" in cfp:
            # taxi-oriented alternative kept available under same label unless override
            pass
        if "高速鐵路運輸服務" in cfp:
            factors["火車/高鐵"] = cfp["高速鐵路運輸服務"]
        if "自用大客車_柴油" in cfp:
            factors["巴士"] = cfp["自用大客車_柴油"]
        # aviation stays screening unless user passes overrides (no national average)
    else:
        raise ValueError(f"unknown factor profile: {profile!r}")

    if overrides:
        factors.update({str(k): float(v) for k, v in overrides.items()})
    return factors


# Module-level default (screening); mutable for advanced callers
CARBON_EMISSION_FACTORS: Dict[str, float] = get_emission_factors("screening")


def set_emission_factors(factors: Mapping[str, float]) -> None:
    """Replace process-wide default factor table (GUI / batch)."""
    CARBON_EMISSION_FACTORS.clear()
    CARBON_EMISSION_FACTORS.update({str(k): float(v) for k, v in factors.items()})


def reload_emission_factors(profile: str = "screening", **kwargs) -> Dict[str, float]:
    factors = get_emission_factors(profile, **kwargs)
    set_emission_factors(factors)
    return dict(CARBON_EMISSION_FACTORS)


def determine_transport_mode(
    travel_type: str,
    distance_km: float,
    *,
    factors: Optional[Mapping[str, float]] = None,
) -> Tuple[str, float]:
    """Infer transport mode and factor from trip type label and distance."""
    table = factors if factors is not None else CARBON_EMISSION_FACTORS
    if distance_km is None or distance_km <= 0:
        return ("N/A", 0.0)

    travel_type = travel_type or ""

    def f(mode: str) -> float:
        return float(table.get(mode, _BUILTIN_FACTORS.get(mode, 0.0)))

    if "國際" in travel_type:
        return ("國際航班", f("國際航班"))
    if "離島" in travel_type or "航班" in travel_type:
        return ("國內航班", f("國內航班"))
    if "開車" in travel_type:
        if distance_km > HSR_DISTANCE_KM:
            return ("火車/高鐵", f("火車/高鐵"))
        return ("自用車/計程車", f("自用車/計程車"))

    if distance_km > DOMESTIC_FLIGHT_DISTANCE_KM:
        return ("國內航班", f("國內航班"))
    if distance_km > HSR_DISTANCE_KM:
        return ("火車/高鐵", f("火車/高鐵"))
    return ("自用車/計程車", f("自用車/計程車"))


def calculate_carbon_emission(
    travel_type: str,
    distance_km: float,
    *,
    factors: Optional[Mapping[str, float]] = None,
) -> Dict[str, object]:
    """Compute CO2e for a single trip leg (distance-based)."""
    transport_mode, factor = determine_transport_mode(
        travel_type, distance_km, factors=factors
    )
    if factor == 0 or distance_km is None or distance_km <= 0:
        emission = 0.0
    else:
        emission = round(float(distance_km) * float(factor), 3)
    return {
        "交通方式": transport_mode,
        "碳排係數": factor,
        "碳排放量(kg CO2e)": emission,
    }


def sensitivity_compare(
    travel_type: str,
    distance_km: float,
) -> Dict[str, Dict[str, object]]:
    """Compare screening vs taiwan_cfp profiles for one leg."""
    a = get_emission_factors("screening")
    b = get_emission_factors("taiwan_cfp")
    return {
        "screening": calculate_carbon_emission(travel_type, distance_km, factors=a),
        "taiwan_cfp": calculate_carbon_emission(travel_type, distance_km, factors=b),
    }

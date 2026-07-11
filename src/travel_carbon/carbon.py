"""Distance-based GHG factors and mode heuristics for business travel.

Aligned with GHG Protocol Scope 3 Category 6 (distance-based method).
Factors are simplified operational defaults used by the desktop tool; see
``docs/emission_factors_notes.md`` for honesty notes vs Taiwan MOENV tables.
"""

from __future__ import annotations

from typing import Dict, Tuple

# Simplified factors (kg CO2e / km). Source note: operational defaults
# historically labeled "環保署 2023-style" in the GUI — verify against
# MOENV 113 announcement before claiming statutory compliance.
CARBON_EMISSION_FACTORS: Dict[str, float] = {
    "自用車/計程車": 0.21,
    "國內航班": 0.133,
    "國際航班": 0.101,
    "火車/高鐵": 0.034,
    "巴士": 0.065,
}

# Heuristic thresholds (km)
HSR_DISTANCE_KM = 300
DOMESTIC_FLIGHT_DISTANCE_KM = 500


def determine_transport_mode(
    travel_type: str, distance_km: float
) -> Tuple[str, float]:
    """Infer transport mode and factor from trip type label and distance.

    Parameters
    ----------
    travel_type:
        Labels such as ``國內-開車``, ``國際-飛行``, ``國內-離島航班``.
    distance_km:
        One-way distance in kilometres.

    Returns
    -------
    (mode_name, factor_kg_per_km)
    """
    if distance_km is None or distance_km <= 0:
        return ("N/A", 0.0)

    travel_type = travel_type or ""

    if "國際" in travel_type:
        return ("國際航班", CARBON_EMISSION_FACTORS["國際航班"])
    if "離島" in travel_type or "航班" in travel_type:
        return ("國內航班", CARBON_EMISSION_FACTORS["國內航班"])
    if "開車" in travel_type:
        if distance_km > HSR_DISTANCE_KM:
            return ("火車/高鐵", CARBON_EMISSION_FACTORS["火車/高鐵"])
        return ("自用車/計程車", CARBON_EMISSION_FACTORS["自用車/計程車"])

    # Default distance heuristic when type is ambiguous
    if distance_km > DOMESTIC_FLIGHT_DISTANCE_KM:
        return ("國內航班", CARBON_EMISSION_FACTORS["國內航班"])
    if distance_km > HSR_DISTANCE_KM:
        return ("火車/高鐵", CARBON_EMISSION_FACTORS["火車/高鐵"])
    return ("自用車/計程車", CARBON_EMISSION_FACTORS["自用車/計程車"])


def calculate_carbon_emission(travel_type: str, distance_km: float) -> Dict[str, object]:
    """Compute CO2e for a single trip leg (distance-based).

    Returns a dict with Chinese keys matching the GUI export columns.
    """
    transport_mode, factor = determine_transport_mode(travel_type, distance_km)
    if factor == 0 or distance_km is None or distance_km <= 0:
        emission = 0.0
    else:
        emission = round(float(distance_km) * float(factor), 3)
    return {
        "交通方式": transport_mode,
        "碳排係數": factor,
        "碳排放量(kg CO2e)": emission,
    }

"""python -m travel_carbon — tiny offline demo CLI."""

from __future__ import annotations

import argparse
import json
import sys


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m travel_carbon",
        description="Offline trip distance + carbon demo (Scope 3 Cat. 6 style)",
    )
    parser.add_argument("destination", nargs="?", default="台中", help="free-text destination")
    parser.add_argument(
        "--profile",
        choices=("screening", "taiwan_cfp"),
        default="screening",
        help="emission factor profile",
    )
    parser.add_argument(
        "--osrm",
        action="store_true",
        help="use public OSRM for mainland driving (needs network)",
    )
    parser.add_argument("--json", action="store_true", help="print JSON")
    args = parser.parse_args(argv)

    from travel_carbon.pipeline import estimate_trip

    result = estimate_trip(
        args.destination,
        use_osrm=args.osrm,
        factor_profile=args.profile,
    )
    if args.json:
        # make JSON-safe (coords may contain nested dicts OK)
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    else:
        d = result["distance"]
        c = result["carbon"]
        print(f"input:      {result['input']}")
        print(f"normalized: {result['normalized']}")
        print(f"kind:       {result['kind']}")
        print(f"type:       {d.get('類型')}")
        print(f"distance:   {d.get('距離(km)')} km")
        print(f"time:       {d.get('時間')}")
        print(f"mode:       {c.get('交通方式')}")
        print(f"factor:     {c.get('碳排係數')} kgCO2e/km  [{result['factor_profile']}]")
        print(f"emission:   {c.get('碳排放量(kg CO2e)')} kgCO2e")
    return 0


if __name__ == "__main__":
    sys.exit(main())

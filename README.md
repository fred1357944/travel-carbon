# travel-carbon

> Distance-based **Scope 3 Category 6** helpers and desktop workflow for **Traditional Chinese** university business-travel ledgers

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## What this is

Open tooling for higher-education staff and researchers who need to turn **messy Excel reimbursement rows** into:

1. **Distances** (OSRM driving for Taiwan mainland; geodesic flight legs for offshore/international)
2. **Map audit trails** (Folium HTML / optional PNG)
3. **CO₂e estimates** (distance × mode factor, GHG Protocol Category 6 *distance-based* style)

Primary context: Taiwan HEI administrative ledgers (e.g. Fu Jen Catholic University workflows).  
This is **not** a full multi-scope campus GHG platform (compare GES 1point5, CO2UNV for broader inventories).

## Install (library + tests)

```bash
python3 -m pip install -e ".[dev]"
pytest -q
python3 -c "from travel_carbon import calculate_carbon_emission as c; print(c('國際-飛行', 1000))"
```

Package code lives in `src/travel_carbon/` (carbon factors, mode heuristics, zoom, place-text helpers).

## Desktop GUI

```bash
python3 travel_distance_calculator_gui_cached_efficient.py
```

Dependencies (if not using the package install):

```bash
python3 -m pip install pandas openpyxl xlsxwriter folium geopy requests pillow
# optional map screenshots:
# python3 -m pip install selenium
```

## Architecture

```
Excel ledger → place normalize / gazetteer → coordinates
            → OSRM (domestic road) | geodesic (island/international air)
            → Folium maps + cache → Excel export + carbon summary
```

| Path | Role |
|------|------|
| `src/travel_carbon/` | Tested library (JOSS packaging core) |
| `travel_distance_calculator_gui_cached_efficient.py` | Primary Tkinter GUI |
| `process_travel_data_AI.py` | Rule-based location extraction CLI (*not* ML) |
| `map_utils.py` | Folium helpers / smart zoom |
| `examples/` | Synthetic demo CSV only |
| `paper/paper.md` | JOSS-style short paper draft |
| `docs/` | Manuals + research notes |

## Emission factors (honesty)

Default kg CO₂e/km values are **simplified operational defaults**.  
See `docs/emission_factors_notes.md` before claiming MOENV statutory compliance.  
Aviation **RFI is not** applied by default.

## Privacy

- Real reimbursement workbooks may contain personal data — **do not commit them**.
- `.gitignore` excludes `*.xlsx` / `maps/` / caches by default.
- Only synthetic examples ship under `examples/`.

## Citation

See `CITATION.cff` and `paper/paper.md`.

```bibtex
@software{lai_travel_carbon,
  title  = {travel-carbon: Distance-based Scope 3 helpers for Chinese university travel ledgers},
  author = {Lai, Hung-Yi},
  year   = {2026},
  version = {0.1.0},
  note   = {Software repository}
}
```

## License

MIT — see `LICENSE`.

## Status

**v0.1.0 alpha** — packaging and unit tests for core pure functions; GUI remains the operational entry point. Path A (JOSS/SoftwareX) engineering is in progress.

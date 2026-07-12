# travel-carbon

> Distance-based **Scope 3 Category 6** helpers and desktop workflow for **Traditional Chinese** university business-travel ledgers

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/fred1357944/travel-carbon/actions/workflows/ci.yml/badge.svg)](https://github.com/fred1357944/travel-carbon/actions/workflows/ci.yml)
[![GitHub](https://img.shields.io/badge/GitHub-fred1357944%2Ftravel--carbon-blue)](https://github.com/fred1357944/travel-carbon)

**Repository:** https://github.com/fred1357944/travel-carbon

## What this is

Open tooling for higher-education staff and researchers who need to turn **messy Excel reimbursement rows** into:

1. **Distances** (OSRM driving for Taiwan mainland; geodesic flight legs for offshore/international)
2. **Map audit trails** (Folium HTML / optional PNG)
3. **CO₂e estimates** (distance × mode factor, GHG Protocol Category 6 *distance-based* style)

Primary context: Taiwan HEI administrative ledgers (e.g. Fu Jen Catholic University workflows).  
This is **not** a full multi-scope campus GHG platform (compare GES 1point5, CO2UNV for broader inventories).

## Install (library + tests)

```bash
# from a clone
git clone https://github.com/fred1357944/travel-carbon.git
cd travel-carbon
python3 -m pip install -e ".[dev]"
pytest -q
python3 -c "from travel_carbon import calculate_carbon_emission as c; print(c('國際-飛行', 1000))"

# offline one-shot demo (no GUI)
python3 -m travel_carbon 台中
python3 -m travel_carbon 日本 --profile taiwan_cfp
python3 -m travel_carbon 金門 --json

# offline gold evaluation (synthetic ~50-row set)
python3 -m travel_carbon.eval_batch \
  --gold examples/sample_travel_gold_50.csv \
  --out-dir outputs/eval
# → kind_accuracy / mode_accuracy + report.md
```

Package code lives in `src/travel_carbon/`:

| Module | Role |
|--------|------|
| `data/` | Gazetteer coordinates, aliases, mappings, `factors.yaml` |
| `locations/` | Free-text resolve / domestic-island-international classify |
| `distance/` | Geodesic + optional OSRM driving |
| `carbon/` | Mode heuristics + factor profiles (`screening` / `taiwan_cfp`) |
| `pipeline` | `estimate_trip()` end-to-end helper |

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
  title   = {travel-carbon: Distance-based Scope 3 helpers for Chinese university travel ledgers},
  author  = {Lai, Hung-Yi},
  year    = {2026},
  version = {0.1.0},
  url     = {https://github.com/fred1357944/travel-carbon}
}
```

## License

MIT — see `LICENSE`.

## Status

**v0.1.0 alpha** — installable library, offline gold eval, CI, JOSS paper draft (`paper/paper.md`). GUI remains the operational batch entry point.

- Checklist: `docs/JOSS_CHECKLIST.md`
- **Zenodo + JOSS submit steps:** `docs/JOSS_SUBMISSION.md`

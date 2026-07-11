# Path A progress log — 2026-07-11

## Done this session

| Item | Evidence |
|------|----------|
| Restore project from Fred 1 | Local 1.0G + external intact |
| Package `src/travel_carbon` | carbon / zoom / geo_text |
| `pyproject.toml` + MIT `LICENSE` | installable `pip install -e ".[dev]"` |
| pytest | **15 passed** |
| GUI imports package with fallback | `travel_distance_calculator_gui_cached_efficient.py` |
| Examples (synthetic only) | `examples/sample_travel_records.csv` |
| JOSS draft | `paper/paper.md` + `paper.bib` |
| CITATION.cff | root |
| Factor honesty | `docs/emission_factors_notes.md` + `data/factors.yaml` |
| git | `main` @ `263ea72` (+ follow-up commit for factor notes) |
| .gitignore | excludes xlsx / maps / caches / intermediate ledgers |

## Parallel agent outputs absorbed

1. **Modularization map** — next extract wave: COORDINATES/ALIASES, smart_destination, distance.compute (offline tests first).  
2. **JOSS paper draft** — complementary framing vs GES1point5 / CO2UNV / Auger.  
3. **MOENV audit** — 113-02-05 is **fuel kg/TJ**, not pkm; only HSR 0.034 clearly matches CFP; car/air defaults must not claim 環境部公告.

## Still open (next loops)

- [ ] Public GitHub remote (user creates; fill PLACEHOLDER URLs)
- [ ] Extract gazetteer + location resolve into package + tests (offline)
- [ ] Optional: load factors from `data/factors.yaml`
- [ ] Anonymized evaluation n=50–100 (not blocking JOSS minimum)
- [ ] Zenodo / archive DOI
- [ ] Author ORCID / affiliation confirm

## Do not

- Commit real `*.xlsx` or `maps/`
- Claim “符合環境部 113 公告” for current defaults
- Submit JOSS before public repo + clean install path verified on a second machine

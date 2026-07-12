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

## Loop 2 — gazetteer extract (2026-07-11, **not git-committed** per user)

| Item | Evidence |
|------|----------|
| `src/travel_carbon/data/` | coordinates / aliases / mappings (from GUI) |
| `src/travel_carbon/locations/resolve.py` | smart_destination_handler, is_domestic, resolve_coordinates, classify_trip_kind |
| GUI slim | ~2469 → **~1451** lines; imports package data + delegates methods |
| Tests | **26 passed** (was 15) via `tests/test_locations.py` |
| Git | working tree dirty; **no commit** (user: 繼續不要進 git) |

## Loop 3 — distance package (2026-07-11, **not git-committed**)

| Item | Evidence |
|------|----------|
| `src/travel_carbon/distance/` | geodesic.py, osrm.py, compute.py |
| Offline API | `compute_driving_distance(..., use_osrm=False)`, island + international flight |
| GUI | three distance methods are thin wrappers; GUI ~**1143** lines |
| Tests | **35 passed** (`tests/test_distance.py`) |
| Git | still **no commit** |

## Loop 4 — factors.yaml + pipeline CLI (2026-07-11, **not git-committed**)

| Item | Evidence |
|------|----------|
| `get_emission_factors("screening"\|"taiwan_cfp")` | YAML-backed; CFP profile drops car 0.21→0.115 |
| `estimate_trip()` | `pipeline.py` offline E2E |
| CLI | `python -m travel_carbon 台中` |
| Tests | **43 passed** |
| Git | **no commit** |

## Loop 5 — offline gold eval + map meta (2026-07-11, **not git-committed**)

| Item | Evidence |
|------|----------|
| `examples/sample_travel_gold.csv` | 10-row gold kinds |
| `python -m travel_carbon.eval_batch` | kind/mode accuracy **1.0** on gold |
| `outputs/eval/report.md` | local artifact (gitignored) |
| empty dest → `unknown` | fixed (was misclassified international) |
| `maps_meta.route_map_meta` | center/zoom without Folium |
| Tests | **47 passed** |
| Git | **no commit** |


## Loop 6 — gold n≈50 + 桃園區映射 (after commit d96d429)

| Item | Evidence |
|------|----------|
| git commit | `d96d429` modular package + eval harness |
| 中壢等 | `TAIWAN_REGION_MAPPING` 桃園/新竹/台中擴充 |
| `examples/sample_travel_gold_50.csv` | **52** rows, kind/mode accuracy **1.0** offline |
| Tests | **48 passed** |


## Loop 7 — JOSS polish (2026-07-11)

| Item | Evidence |
|------|----------|
| `paper/paper.md` | Rewritten with library API + gold *n*=52 QA; factor honesty |
| `paper/paper.bib` | Added Valls-Val 2021, Kiehle, Tsai 2025, Lee 2021 |
| `docs/JOSS_CHECKLIST.md` | Submission gate list |
| `.github/workflows/ci.yml` | pytest + offline eval on 3.10/3.12 |
| Import warning | `evaluate_gold_csv` no longer eagerly imported in `__init__` |


## Loop 8 — public GitHub via `gh` (2026-07-11)

| Item | Evidence |
|------|----------|
| Repo | https://github.com/fred1357944/travel-carbon |
| Push | `main` + tag `v0.1.0` |
| Release | https://github.com/fred1357944/travel-carbon/releases/tag/v0.1.0 |
| CI | **success** (Python 3.10 + 3.12) |



## Loop 9 — Zenodo/JOSS submission guide (2026-07-12)

| Item | Evidence |
|------|----------|
| `docs/JOSS_SUBMISSION.md` | Zenodo link steps + JOSS form checklist + post-DOI commands |
| paper date | 12 July 2026; `archive_doi` placeholder commented |
| Blocker for submit | User Zenodo OAuth + ORCID (browser) |



## Loop 10 — application venue track (2026-07-12)

| Item | Evidence |
|------|----------|
| Venue matrix | `docs/VENUE_MATRIX_travel_carbon.md` (IJSHE AMBER, Sustainability AMBER, JOSS backup) |
| VENUE_LEDGER | travel-carbon row + decision log in `論文撰寫專案/VENUE_LEDGER.md` |
| Literature | `paper/references.bib` ~28 keys + `CITATIONS_VERIFIED.md` |
| Long draft | `paper/application_draft.md` |
| Rendered refs | `paper/build/application_draft.html` (pandoc --citeproc) |


## Still open (next loops)

- [x] **Public GitHub remote**: https://github.com/fred1357944/travel-carbon
- [x] Extract gazetteer + location resolve into package + tests (offline)
- [x] Extract distance helpers (geodesic / OSRM client) with offline geodesic tests
- [x] Load factors from `factors.yaml` + sensitivity profile
- [x] Offline gold eval harness (*n*≈52 synthetic)
- [x] JOSS paper draft + checklist + CI workflow file
- [ ] Optional full Folium map builder extract (low priority)
- [ ] Larger anonymized evaluation on real-like ledgers
- [ ] Zenodo / archive DOI
- [ ] Author ORCID / affiliation confirm

## Do not

- Commit real `*.xlsx` or `maps/`
- Claim “符合環境部 113 公告” for current defaults
- Submit JOSS before public repo + clean install path verified on a second machine
- Auto-commit while user said 不要進 git

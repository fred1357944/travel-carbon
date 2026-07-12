# JOSS readiness checklist (Path A)

Status snapshot: **2026-07-12**, package `travel-carbon` **v0.1.0**,  
public repo https://github.com/fred1357944/travel-carbon  
Full submit steps: **`docs/JOSS_SUBMISSION.md`**.

## Required for submission

| Item | Status | Notes |
|------|--------|-------|
| Open-source license | ✅ | MIT `LICENSE` |
| Public repository | ✅ | https://github.com/fred1357944/travel-carbon |
| Installable package | ✅ | `pip install -e ".[dev]"` / `pyproject.toml` |
| Automated tests | ✅ | `pytest` — 48 passed |
| Example that runs | ✅ | `python -m travel_carbon 台中`; `examples/` |
| `paper/paper.md` | ✅ | JOSS-style draft |
| Statement of need | ✅ | Complements GES1point5 / CO2UNV / Auger |
| CITATION.cff | ✅ | Root |
| No secrets / PII in repo | ✅ | `.gitignore` blocks `*.xlsx`, `maps/`, `outputs/` |
| GitHub Release tag | ✅ | [v0.1.0](https://github.com/fred1357944/travel-carbon/releases/tag/v0.1.0) |
| CI green | ✅ | Actions: pytest + offline eval on 3.10/3.12 |
| Archive (Zenodo) DOI | ❌ | Optional next: Zenodo from GitHub release |

## Recommended before review

| Item | Status | Notes |
|------|--------|-------|
| CI (GitHub Actions) | ✅ | `.github/workflows/ci.yml` (runs when remote exists) |
| Offline gold eval | ✅ | `sample_travel_gold_50.csv` kind/mode = 1.0 |
| Emission-factor honesty | ✅ | `docs/emission_factors_notes.md` |
| GUI still runnable | ✅ | `travel_distance_calculator_gui_cached_efficient.py` |
| CONTRIBUTING / issue template | ✅ | CONTRIBUTING.md + bug template |
| ORCID / affiliation confirm | ⚠️ | Author placeholder fields in paper front matter |
| Institutional consent wording | ⚠️ | Fu Jen case only if approved |

## Commands reviewers can run

```bash
python3 -m pip install -e ".[dev]"
pytest -q
python3 -m travel_carbon 台中
python3 -m travel_carbon.eval_batch \
  --gold examples/sample_travel_gold_50.csv \
  --out-dir /tmp/travel-carbon-eval
```

## Do not claim in paper/review replies

- “AI / LLM extraction”
- “Compliant with MOENV 113 fuel gazette” for screening km factors
- “First university carbon tool in the world”
- Meter-level distance accuracy without validation study
